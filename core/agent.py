import os
import csv
from core.document_processor import DocumentProcessor
from core.services.ollama import OllamaService


class DocumentAgent:
    def __init__(self, processor: DocumentProcessor, ollama: OllamaService):
        self.processor = processor
        self.ollama = ollama

    def process_pdf(self, pdf_path: str, output_csv: str, mode: str = "vl"):
        pages = self.processor.pdf_to_images(pdf_path)
        results = []

        for page_num, img in pages:
            print(f"\n Page {page_num} → OCR")
            text = self.processor.ocr_image(img)

            if self.processor.contains_invoice_keywords(text):
                print(f" Invoice Keywords Found → Sending to {mode.upper()} model")
                result = self.ollama.query_vl(img) if mode == "vl" else self.ollama.query_llm(text)
            else:
                result = "NO INVOICE DETECTED"

            results.append({"page": page_num, "output": result})

        self._save_csv(results, output_csv)
        print(f"Done: {output_csv}")

    def _save_csv(self, results, output_csv):
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Page Number", "Extracted JSON or Message"])
            for row in results:
                writer.writerow([row["page"], row["output"]])
