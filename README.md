# Request for Proposal (RFP) Extraction Tool

Request for Proposal (RFP) Extraction Tool is an end-to-end automated system designed to intelligently extract and structure key information from RFP and Bid documents of varying formats -  including [...]

Organizations, especially those in procurement, education, and government sectors, often deal with large volumes of RFPs that contain crucial details like Bid Numbers, Submission Deadlines, Payment Te[...]

## Features

- Multi-format document support (PDF, HTML, DOCX, TXT)
- Intelligent text chunking for better processing
- Hybrid extraction engine combining rule-based and ML approaches
- Automated field extraction for standardized RFP information
- JSON output for structured data storage

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Google Cloud project with Gemini API access

### Installation and Setup

#### Option 1: Clone from GitHub

1. **Clone the repository**
   ```bash
   git clone https://github.com/hagNone/Request_for_proposal_extraction.git
   cd Request_for_proposal_extraction
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Gemini API**

   Choose one of these methods to set your API key:

   ```powershell
   # In PowerShell
   $env:GOOGLE_API_KEY = "your_api"
   ```

   ```bash
   # In Windows Command Prompt
   set GOOGLE_API_KEY=your_gemini_api_key

   # In macOS/Linux Terminal
   export GOOGLE_API_KEY=your_gemini_api_key
   ```

   Or create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   ```

#### Option 2: If You Have the Full Code as a ZIP File

If you received the project as a ZIP file (instead of cloning from GitHub):

1. **Extract the ZIP file**
   - Right-click the ZIP file and choose "Extract All" (Windows) or use `unzip filename.zip` (macOS/Linux).
   - Move into the extracted folder:
     ```bash
     cd Request_for_proposal_extraction
     ```

2. **Create and activate a virtual environment**
   - See instructions above for your operating system.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Gemini API**
   - Follow instructions above to set the API key.

5. **Run the tool**
   ```bash
   python -m src.core.controllers
   ```

### Verification

To verify your setup:

1. Ensure your virtual environment is activated (you should see `(venv)` in your terminal)
2. Run a quick test:
   ```bash
   python -c "import pdfplumber; import google.generativeai; print('Setup successful!')"
   ```

3. Verify your API key is set:
   ```powershell
   # In PowerShell
   echo $env:google_api
   ```

## Project Structure

```
├── src/
│   ├── core/
│   │   └── controllers.py      # Main pipeline control and orchestration
│   ├── parsers/
│   │   └── pdf_parser.py       # Document parsing for multiple formats
│   ├── preprocessors/
│   │   └── chunker.py          # Text chunking and segmentation
│   ├── extraction/
│   │   └── hybrid_engine.py    # Extraction logic implementation
│   ├── llm_api/
│   │   └── prompt_templates.py # LLM integration for extraction
│   ├── postprocessors/
│   │   └── validator.py        # Output validation and serialization
│   └── schemas/
│       └── rfp_schema.py       # Data schemas for RFP fields
├── data/
│   └── raw_documents/          # Input RFP documents
└── outputs/                    # Processed JSON outputs
```

## How It Works

1. **Document Parsing (`parsers/pdf_parser.py`)**:
   - Supports multiple file formats (PDF, HTML, DOCX, TXT)
   - Extracts readable text while preserving document structure
   - Performs initial text cleaning and normalization

2. **Text Chunking (`preprocessors/chunker.py`)**:
   - Splits documents into semantic chunks (~1500 characters)
   - Preserves section boundaries and context
   - Handles overlapping content for better extraction

3. **Information Extraction (`core/controllers.py`)**:
   - Processes individual files through the extraction pipeline
   - Merges results from multiple documents
   - Manages the overall extraction workflow

4. **AI-Powered Extraction (`llm_api/prompt_templates.py`)**:
   - Uses Gemini AI model for intelligent field extraction
   - Implements structured prompts for consistent results
   - Handles error cases and ensures complete field coverage

5. **Validation and Output (`postprocessors/validator.py`)**:
   - Validates extracted data against defined schemas
   - Serializes results to standardized JSON format
   - Ensures data quality and consistency

## Usage

1. Place your RFP documents in the `data/raw_documents/` directory, organized by bid folders

2. Run the main processing pipeline:
```python
python -m src.core.controllers
```

3. Find processed results in the `outputs/` directory as JSON files

## Output Format

The tool extracts standardized fields from RFP documents and outputs them in a structured JSON format. Each bid folder's documents are processed and consolidated into a single JSON file containing all[...]

## Dependencies

Key dependencies include:
- pdfplumber: PDF text extraction
- BeautifulSoup4: HTML parsing
- python-docx: DOCX file processing
- langchain: Text chunking and processing
- google.generativeai: Gemini API integration

Full dependencies are listed in `requirements.txt`.

## Troubleshooting

Common issues and solutions:

1. **Gemini API Authentication Error**
   - Verify your API key is set correctly: `echo $env:google_api` in PowerShell
   - Check if your Google Cloud project has the Gemini API enabled
   - Ensure you have proper billing set up in Google Cloud

2. **PDF Processing Issues**
   - Make sure your PDFs are text-based and not scanned images
   - Check if pdfplumber is properly installed
   - Try upgrading pdfplumber if you encounter version conflicts

3. **Virtual Environment Problems**
   - Ensure you're in the correct directory when creating the venv
   - Verify the virtual environment is activated
   - Try recreating the virtual environment if dependencies conflict

## Maintainer

- GitHub: [@hagNone](https://github.com/hagNone)

## License

MIT License