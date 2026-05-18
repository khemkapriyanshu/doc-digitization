import fitz
from PIL import Image
import pytesseract
from typing import List, Tuple


class DocumentProcessor:
    def __init__(self, dpi: int, keywords: List[str]):
        self.dpi = dpi
        self.keywords = [k.lower() for k in keywords]

    def pdf_to_images(self, pdf_path: str) -> List[Tuple[int, Image.Image]]:
        doc = fitz.open(pdf_path)
        pages = []
        for i, page in enumerate(doc):
            mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pages.append((i + 1, img))
        doc.close()
        return pages

    def ocr_image(self, image: Image.Image) -> str:
        return pytesseract.image_to_string(image)

    def contains_invoice_keywords(self, text: str) -> bool:
        return any(k in text.lower() for k in self.keywords)
