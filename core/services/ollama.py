import ollama
from io import BytesIO
from PIL import Image


class OllamaService:
    def __init__(self, vl_model: str, llm_model: str):
        self.vl_model = vl_model
        self.llm_model = llm_model

        self.vl_prompt = """
        You are an invoice extraction agent.
        Given an image of a document page, extract a valid JSON containing:
        Invoice Number, Date, Seller, GSTIN, Items, Tax, Amount.
        """

        self.llm_prompt = """
        You are an invoice extraction agent.
        Given a plain text, extract and return a valid JSON containing:
        Invoice Number, Date, Seller, GSTIN, Items, Tax, Amount.
        """

    def query_vl(self, image: Image.Image) -> str:
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        response = ollama.chat(
            model=self.vl_model,
            messages=[
                {"role": "system", "content": self.vl_prompt},
                {"role": "user", "content": "", "images": [img_bytes]}
            ]
        )
        return response["message"]["content"].strip()

    def query_llm(self, text: str) -> str:
        response = ollama.chat(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": self.llm_prompt},
                {"role": "user", "content": text}
            ]
        )
        return response["message"]["content"].strip()
