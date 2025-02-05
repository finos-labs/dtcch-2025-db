# PDF Analysis Tool

A powerful tool that leverages AWS Bedrock's Claude model to analyze PDF documents, extract content, and generate structured analysis. The tool processes PDFs page by page, generating labels and comprehensive summaries while handling both text and images.

## Features

- **Page-by-Page Analysis**: Process specific pages, page ranges, or entire documents
- **Intelligent Content Analysis**: Uses AWS Bedrock's Claude model to:
  - Generate up to 5 relevant topic labels per page
  - Create comprehensive summaries capturing key information
- **Image Support**: Extracts and processes images within PDFs
- **Flexible Output**: Generates CSV files with structured analysis
- **Progress Tracking**: Shows real-time processing status

## Prerequisites

1. Python 3.8+
2. AWS Account with Bedrock access
3. AWS credentials configured with appropriate permissions
4. Required Python packages (install via requirements.txt)

## Installation

1. Ensure you have the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_SESSION_TOKEN=your_session_token  # if using temporary credentials
```

## Usage

### Basic Usage

1. Process all pages in a PDF:
```bash
python pdf_handler.py --examples_pdf path/to/your.examples_pdf
```

2. Process specific pages:
```bash
python pdf_handler.py --examples_pdf path/to/your.examples_pdf --pages 1,3,5
```

3. Process a range of pages:
```bash
python pdf_handler.py --examples_pdf path/to/your.examples_pdf --pages 1-5
```

4. Specify custom output location:
```bash
python pdf_handler.py --examples_pdf path/to/your.examples_pdf --output custom/path/analysis.csv
```

### Command Line Arguments

| Argument | Short | Required | Description | Example |
|----------|--------|-----------|-------------|---------|
| --pdf | -p | Yes | Path to the PDF file | --pdf docs/report.pdf |
| --pages | -pg | No | Pages to process | --pages 1,3,5 or --pages 1-5 or --pages all |
| --output | -o | No | Output CSV path | --output analysis/result.csv |

### Output Format

The tool generates a CSV file with the following columns:

1. **PDF_Name**: Name of the processed PDF file
2. **Page_Number**: Page number being analyzed
3. **Labels**: Up to 5 topic labels (semicolon-separated)
4. **Summary**: Comprehensive page summary

Example output:
```csv
PDF_Name,Page_Number,Labels,Summary
report.pdf,1,"executive summary; financial results; Q4 2024","This page contains the executive summary..."
report.pdf,2,"market analysis; competitors; growth","Detailed market analysis shows..."
```

## Output Directory Structure

```
tools/
├── output/           # Default output directory
│   └── analysis_TIMESTAMP.csv  # Generated analysis files
├── pdf_handler.py    # Main tool script
└── README.md        # This documentation
```

## Error Handling

The tool includes robust error handling for common issues:

- Invalid PDF paths
- AWS credential issues
- Malformed page ranges
- PDF processing errors
- Image extraction failures

Error messages will provide clear information about what went wrong and how to fix it.

## Best Practices

1. **Page Selection**:
   - Process specific pages when analyzing large documents
   - Use page ranges for sequential analysis
   - Use 'all' only for smaller documents

2. **Output Management**:
   - Use descriptive output filenames
   - Organize outputs in separate directories for different analyses
   - Keep original PDFs in a separate directory

3. **AWS Credentials**:
   - Ensure credentials are properly configured
   - Use environment variables or AWS credential files
   - Verify Bedrock API access before processing large documents

## Troubleshooting

1. **AWS Credentials Error**:
   ```
   Error initializing AWS Bedrock client
   ```
   - Check AWS credentials are properly configured
   - Verify Bedrock API access permissions

2. **PDF Processing Error**:
   ```
   Error processing PDF
   ```
   - Verify PDF file exists and is readable
   - Check PDF is not corrupted or password-protected

3. **Output Directory Error**:
   ```
   Error writing to output file
   ```
   - Verify write permissions in output directory
   - Check disk space availability

## Contributing

Feel free to submit issues and enhancement requests. We welcome contributions to improve the tool.

## License

This tool is part of the FINOS DTCC Hackathon project and is distributed under the Apache License, Version 2.0.
