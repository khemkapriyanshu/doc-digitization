# doc-digitization

This project provides an end-to-end document automation pipeline for structured data extraction from documents like invoices and receipts. It uses Optical Character Recognition (OCR) combined with local Large Language Models (LLMs) to perform intelligent, layout-independent form parsing. The system is designed to run entirely offline, ensuring data privacy and functionality in remote environments.

## Features

- **Structured Data Extraction:** Parses documents like invoices, bills, and receipts to extract key information into a structured JSON format.
- **OCR Integration:** Converts PDF pages into images and uses Tesseract for robust text extraction.
- **Dual-Mode Processing:**
    - **Vision Language Model (VLM) Mode (`vl`):** Directly analyzes document images, preserving layout information for potentially higher accuracy.
    - **Large Language Model (LLM) Mode (`llm`):** Processes OCR-extracted text for a faster, text-only approach.
- **Offline First:** Leverages locally running models via Ollama, ensuring data privacy and eliminating reliance on cloud services.
- **Keyword-Based Filtering:** Intelligently scans documents for specific keywords (e.g., 'invoice', 'gstin') to identify and process only relevant pages.
- **Simple CLI Interface:** A straightforward command-line tool for easy execution and integration into other workflows.

## Setup and Installation

### Prerequisites

- Python 3.x
- [Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract)
- [Ollama](https://ollama.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/khemkapriyanshu/doc-digitization.git
cd doc-digitization
```

### 2. Install Dependencies

Install the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

`pytesseract` is a Python wrapper for Google's Tesseract-OCR Engine, which must be installed on your system.

- **macOS:** `brew install tesseract`
- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
- **Windows:** Download the installer from the [Tesseract at UB Mannheim GitHub page](https://github.com/UB-Mannheim/tesseract/wiki).

### 4. Install and Run Ollama

This tool uses a local Ollama instance for model inference.

1.  Download and install Ollama from [ollama.com](https://ollama.com).
2.  Pull the required models specified in `config/settings.yaml`:

    ```bash
    ollama pull qwen2.5vl:3b
    ollama pull gemma3n:e2b
    ```

3.  Ensure the Ollama application is running before executing the script.

## Configuration

The application's behavior is controlled by the `config/settings.yaml` file.

-   **`general`**
    -   `dpi`: The resolution (dots per inch) for converting PDF pages to images. Higher values improve OCR quality but increase processing time.
    -   `keywords`: A list of terms used to identify relevant documents (e.g., invoices) for processing by the LLM.
-   **`models`**
    -   `vl_model`: The Vision Language Model used for image-based extraction (`--mode vl`).
    -   `llm_model`: The Language Model used for text-based extraction (`--mode llm`).

## Usage

The primary interface is the command-line script `cli.py`.

### Arguments

-   `--input`: Path to the input PDF file.
-   `--output`: Path for the output CSV file.
-   `--mode`: The processing mode. Choose between `vl` (Vision Language Model) or `llm` (standard LLM).

### Examples

**1. Process a PDF using the Vision Language Model (VLM)**

This mode sends the document *image* directly to the model, which is often better at understanding complex layouts.

```bash
python cli.py --input "./inputs/test.pdf" --output "./outputs/output_vl.csv" --mode vl
```

**2. Process a PDF using the standard Large Language Model (LLM)**

This mode runs OCR first and sends the extracted *text* to the model.

```bash
python cli.py --input "./inputs/test.pdf" --output "./outputs/output_llm.csv" --mode llm
```

The script will generate a CSV file at the specified output path containing the page number and the extracted JSON data or a message indicating that no invoice was detected.

## How It Works

1.  **PDF to Image:** The input PDF is loaded, and each page is converted into a high-resolution image.
2.  **OCR Processing:** Tesseract OCR extracts all text from each page image.
3.  **Keyword Detection:** The extracted text is scanned for the keywords defined in `config/settings.yaml`.
4.  **Model Inference:** If keywords are found, the page is passed to the appropriate Ollama model based on the selected mode:
    -   In **`vl` mode**, the page image is sent to the Vision Language Model.
    -   In **`llm` mode**, the OCR-extracted text is sent to the Language Model.
5.  **Data Structuring:** The model is prompted to return the extracted information as a structured JSON object.
6.  **Output Generation:** The results for all pages are compiled and saved into a single CSV file.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.