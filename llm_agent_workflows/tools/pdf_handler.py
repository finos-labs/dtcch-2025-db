import io
import base64
import os
import csv
import time
import fitz  # PyMuPDF

from typing import List, Dict, Union, Optional
from pathlib import Path
from PIL import Image

from agents.agent_filter_policy import AgentFilterPolicy

class PDFHandler:
    def __init__(self):
        """Initialize the PDF Handler with AWS Bedrock client."""
        self.agent = AgentFilterPolicy()

    def _extract_text_and_images(self, page) -> Dict[str, Union[str, List[str]]]:
        """Extract both text and images from a PDF page."""
        text = page.get_text()
        processed_images = []

        try:
            # Extract images
            image_list = page.get_images()

            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = fitz.Pixmap(page.parent, xref)

                    # Skip images with alpha channel or CMYK color space
                    if base_image.n - base_image.alpha > 3:
                        base_image = fitz.Pixmap(fitz.csRGB, base_image)

                    # Skip if image data is invalid
                    if base_image.stride < 1 or base_image.width < 1 or base_image.height < 1:
                        print(f"Skipping invalid image {img_index}")
                        continue

                    # Convert to PIL Image
                    img_data = base_image.tobytes()
                    img_size = (base_image.width, base_image.height)

                    if not img_data:
                        print(f"Skipping empty image {img_index}")
                        continue

                    pil_image = Image.frombytes("RGB", img_size, img_data)

                    # Convert to base64
                    buffered = io.BytesIO()
                    pil_image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    processed_images.append(img_str)

                except Exception as e:
                    print(f"Skipping image {img_index} due to error: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error processing images: {str(e)}")

        return {
            "text": text,
            "images": processed_images
        }

    def process_pdf(self,
                   pdf_path: str, 
                   output_path: str = None,
                   page_range: Optional[Union[List[int], tuple]] = None) -> None:
        """Process a PDF file and generate analysis in CSV format."""
        try:
            # Open PDF
            doc = fitz.open(pdf_path)
            pdf_name = Path(pdf_path).name
            
            # Determine pages to process
            if page_range is None:
                pages_to_process = range(len(doc))
            elif isinstance(page_range, tuple):
                start, end = page_range
                pages_to_process = range(start - 1, min(end, len(doc)))
            else:
                pages_to_process = [p - 1 for p in page_range if 0 < p <= len(doc)]
            
            # Generate default output path if not specified
            if output_path is None:
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                output_path = f"tools/output/analysis_{timestamp}.csv"
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Process pages and write to CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['PDF_Name', 'Page_Number', 'Labels', 'Summary'])
                
                for page_idx in pages_to_process:
                    print(f"Processing page {page_idx + 1}...")
                    page = doc[page_idx]
                    content = self._extract_text_and_images(page)
                    analysis = self.agent._analyze_page(content, page_idx + 1)
                    
                    writer.writerow([
                        pdf_name,
                        page_idx + 1,
                        '; '.join(analysis.get('labels', [])),
                        analysis.get('summary', '')
                    ])
                    
            print(f"Analysis complete. Output saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
        finally:
            if 'doc' in locals():
                doc.close()
