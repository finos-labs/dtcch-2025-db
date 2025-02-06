# LLM policy extractor
## Overview
`main.py` is a script designed to extract policies from PDF documents using a language model. It takes a PDF file as input and processes specified pages to extract relevant policy information.

## Arguments
- `--policy_pdf` or `-p`: Path to the PDF file containing the policy document.
- `--variable_references_path` or `-v`: Path to the directory containing the variables reference.
- `--pages` or `-pg`: Pages to be processed. This can be a single page, a range of pages (e.g., 5-7), or a list of pages (e.g., 1,6,9).

## Example Usages
```bash
python main.py --policy_pdf ./examples_pdf/JMLSG-Guidance-Part-I_July-2022.pdf -v ./tools/input/variables_reference --pages 5-7
```
```bash
python main.py --policy_pdf ./examples_pdf/JMLSG-Guidance-Part-I_July-2022.pdf -v ./tools/input/variables_reference --pages 9,13
```
```bash
python main.py --policy_pdf ./examples_pdf/JMLSG-Guidance-Part-I_July-2022.pdf -v ./tools/input/variables_reference --pages 26
```
```bash
python main.py --policy_pdf ./examples_pdf/JMLSG-Guidance-Part-I_July-2022.pdf -v ./tools/input/variables_reference
```

## Output
The script will output the extracted policy information to the console or a specified output file.

## Dependencies
- Python >3.10
- Required Python packages (listed in `requirements.txt`)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/dtcch-2025-db.git
    ```
2. Navigate to the project directory:
    ```bash
    cd dtcch-2025-db/llm_agent_workflows
    ```
3. Install the required packages:
    ```bash
    pip install .
    ```

## Notes
- Ensure that the PDF file and variables reference directory exist and are accessible.
- The script can handle various page specifications, allowing flexibility in processing specific parts of the document.

## Troubleshooting
- If the script fails to run, check the paths to the PDF file and variables reference directory.
- Ensure that all dependencies are installed correctly.
- Refer to the error messages for specific issues and solutions.