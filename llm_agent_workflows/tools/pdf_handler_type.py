import io
import base64
import os
import re
import json
import fitz  # PyMuPDF
from typing import List, Dict, Union, Optional
from pydantic import BaseModel, ConfigDict, ValidationError, TypeAdapter
from pathlib import Path
from PIL import Image

from agents.agent_filter_policy import AgentFilterPolicy

class Sentence(BaseModel):
    model_config = ConfigDict(strict=True)
    sentence_number: int
    sentence: str
    type_of_sentence: str
    page_number: int

ta = TypeAdapter(List[Sentence])

class PDFHandlerType:
    def __init__(self):
        """Initialize the PDF Handler with AWS Bedrock client."""
        self.agent = AgentFilterPolicy()
        self.kyc_keywords = [
            "customer due diligence", "party/parties", "business relationship established",
            "transaction carried out", "beneficial owner/ownership", "acting on own behalf",
            "on whose behalf", "Politically Exposed Person", "PEP", "relatives", "close associates",
            "prominent public function(s)", "heads of state", "heads of government", "ministers",
            "international organisation", "courts of auditors", "central banks",
            "parliaments", "legislative bodies", "supreme courts", "constitutional courts",
            "high-level judicial bodies", "state-owned enterprises", "source of wealth",
            "source of funds", "asset declarations", "income declarations",
            "senior management approval", "Enhanced Due Diligence", "EDD",
            "risk assessment", "risk rating", "high", "medium", "low",
            "geographical risk", "country risk", "product risk", "service risk",
            "delivery channel risk", "transaction patterns", "transaction volumes",
            "ownership structure", "control structure", "company's capital", "company's profit",
            "voting rights", "share/shares", "nominee shareholder/shareholders", "directors",
            "registered address", "principal place of business", "nature of business",
            "certificate of incorporation", "commercial register extract", "articles of association",
            "governing documents", "financial statements", "gross profit", "income", "total assets",
            "family circumstances", "immigration status", "occupation", "employment",
            "financial/banking relationships", "original documents", "copy documents"
        ]

        self.allowed_categories = [
            "Background Information",
            "Definition",
            "Other",
            "KYC Profile Relevant",
            "Organizational Requirement"
        ]

    def _extract_text_and_images(self, page) -> Dict[str, Union[str, List[str]]]:
        """Extract both text and images from a PDF page."""
        text = page.get_text()
        processed_images = []

        try:
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = fitz.Pixmap(page.parent, xref)
                    if base_image.n - base_image.alpha > 3:
                        base_image = fitz.Pixmap(fitz.csRGB, base_image)
                    if base_image.stride < 1 or base_image.width < 1 or base_image.height < 1:
                        print(f"Skipping invalid image {img_index}")
                        continue
                    img_data = base_image.tobytes()
                    img_size = (base_image.width, base_image.height)
                    pil_image = Image.frombytes("RGB", img_size, img_data)
                    buffered = io.BytesIO()
                    pil_image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    processed_images.append(img_str)
                except Exception as e:
                    print(f"Skipping image {img_index} due to error: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error processing images: {str(e)}")

        return {"text": text, "images": processed_images}

    def _analyze_page_with_llm(self, page_text: str, page_num: int) -> List[Dict[str, str]]:
        """Use LLM to analyze the entire page content and extract KYC-relevant sentences."""
        # Clean the text to avoid JSON parsing issues
        clean_text = page_text.replace('\n', ' ').replace('\r', ' ').replace('"', '\\"').strip()
        
        prompt = f"""You are an expert in Know Your Customer (KYC) and Anti-Money Laundering (AML) regulations. Analyze this page content and return ONLY a JSON array of KYC-relevant sentences.

EXTREMELY IMPORTANT: Your response must be a valid JSON array wrapped in ```json and ``` markers.
Do not include ANY other text before or after these markers.

For each KYC-relevant sentence found, include these exact fields:
{{
    "sentence_number": (integer),
    "sentence": (the complete sentence text),
    "type_of_sentence": "KYC Profile Relevant",
    "page_number": {page_num}
}}

Content to analyze:
{clean_text}

Rules:
1. Return ONLY sentences related to:
   - Customer identification/verification
   - Due diligence procedures
   - Risk assessment
   - Transaction monitoring
   - Beneficial ownership
   - PEP screening
   - AML/CTF controls
2. Include the page_number field for each sentence
3. Only use "KYC Profile Relevant" as type_of_sentence
4. If no relevant sentences found, return an empty array []

Example of EXACT expected response format:
```json
[
    {{
        "sentence_number": 1,
        "sentence": "The firm must verify customer identity before establishing a business relationship.",
        "type_of_sentence": "KYC Profile Relevant",
        "page_number": 1
    }}
]
```

YOUR RESPONSE MUST START WITH ```json AND END WITH ``` WITH NO OTHER TEXT."""

        try:
            response = self.agent.invoke_bedrock(prompt)
            
            # Extract JSON array from response using markers
            response = response.strip()
            json_marker = "```json"
            end_marker = "```"
            
            start_idx = response.find(json_marker)
            if start_idx != -1:
                start_idx += len(json_marker)
                end_idx = response.find(end_marker, start_idx)
                if end_idx != -1:
                    json_str = response[start_idx:end_idx].strip()
                    try:
                        sentences = json.loads(json_str)
                        if not isinstance(sentences, list):
                            sentences = [sentences]
                        ta.validate_python(sentences)
                        
                        # Validate each sentence
                        validated_sentences = []
                        for sentence in sentences:
                            if all(key in sentence for key in ["sentence_number", "sentence", "type_of_sentence", "page_number"]):
                                if sentence["type_of_sentence"] == "KYC Profile Relevant":
                                    validated_sentences.append(sentence)
                        
                        return validated_sentences
                    except (json.JSONDecodeError, ValidationError) as je:
                        print(f"JSON parsing error on page {page_num}: {str(je)}")
                        print(f"Attempted to parse: {json_str}")
                        return []
            
            print(f"No valid JSON markers found in response for page {page_num}")
            print(f"Raw response: {response}")
            return []

        except Exception as e:
            print(f"Error analyzing page {page_num}: {str(e)}")
            print(f"Raw response: {response}")
            return []

    def process_pdf_to_json(self, pdf_path: str, output_path: Optional[str] = None, pages: Optional[Union[List[int], tuple]] = None) -> List[Dict]:
        """Process PDF pages and save KYC-relevant sentences to JSON."""
        try:
            print(f"Opening PDF file: {pdf_path}")
            doc = fitz.open(pdf_path)
            pdf_name = Path(pdf_path).name
            total_pages = len(doc)
            print(f"Total pages in PDF: {total_pages}")

            # Determine which pages to process
            if pages is None:
                pages_to_process = range(total_pages)
            elif isinstance(pages, tuple):
                start, end = pages
                pages_to_process = range(start - 1, min(end, total_pages))
            else:
                pages_to_process = [p - 1 for p in pages if 1 <= p <= total_pages]

            all_sentences = []
            for page_num in pages_to_process:
                print(f"Processing page {page_num + 1}")
                page = doc[page_num]
                
                # Extract text from the page
                page_text = page.get_text()
                if not page_text.strip():
                    print(f"No text found on page {page_num + 1}")
                    continue

                # Analyze the page content
                sentences = self._analyze_page_with_llm(page_text, page_num + 1)
                
                # Add metadata to each sentence
                for sentence in sentences:
                    sentence["pdf_name"] = pdf_name
                    all_sentences.append(sentence)

            # Save results to JSON file
            if output_path:
                # Ensure the output directory exists
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                
                # Add .json extension if not present
                if not output_path.endswith('.json'):
                    output_path = output_path + '.json'
                
                # Write the results
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(all_sentences, f, indent=4, ensure_ascii=False)
                print(f"Output saved to: {output_path}")
                print(f"Found {len(all_sentences)} KYC-relevant sentences across {len(pages_to_process)} pages")

            return all_sentences

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

def main():
    """Main function to handle command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process a PDF file for text and image extraction with classification.')
    parser.add_argument('--examples_pdf', required=True, help='Path to the PDF file')
    parser.add_argument('--output', help='Output JSON file path (optional)')
    parser.add_argument('--pages', help='Page range (e.g., "1-20" or "1,2,3")')
    
    args = parser.parse_args()
    
    # Parse page range if provided
    pages = None
    if args.pages:
        if '-' in args.pages:
            start, end = map(int, args.pages.split('-'))
            pages = (start, end)
        else:
            pages = [int(p) for p in args.pages.split(',')]
    
    handler = PDFHandlerType()
    result = handler.process_pdf_to_json(args.examples_pdf, args.output, pages)
    
    if not args.output:
        print("Output will be returned as JSON object (no file saved).")
        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()