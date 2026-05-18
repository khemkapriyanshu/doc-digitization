import argparse
import yaml
from core.document_processor import DocumentProcessor
from core.services.ollama import OllamaService
from core.agent import DocumentAgent


def load_config(path="config/settings.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    parser = argparse.ArgumentParser(description="Document Agent")
    parser.add_argument("--input", required=True, help="Input PDF path")
    parser.add_argument("--output", required=True, help="CSV output path")
    parser.add_argument("--mode", default="vl", choices=["vl", "llm"], help="Choose mode: 'vl' or 'llm'")
    args = parser.parse_args()

    processor = DocumentProcessor(dpi=config["general"]["dpi"], keywords=config["general"]["keywords"])
    ollama = OllamaService(
        vl_model=config["models"]["vl_model"],
        llm_model=config["models"]["llm_model"]
    )

    agent = DocumentAgent(processor, ollama)
    agent.process_pdf(args.input, args.output, mode=args.mode)


if __name__ == "__main__":
    main()


