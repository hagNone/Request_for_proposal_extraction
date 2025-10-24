from pathlib import Path
import json
from src.parsers.pdf_parser import parse_document
from src.preprocessors.chunker import semantic_chunker
from src.extraction.hybrid_engine import hybrid_extract

def process_single_file(file_path):
    """Parse, clean, chunk, and extract fields from a single file."""
    text = parse_document(file_path)
    if not text.strip():
        print(f"No text extracted from {file_path.name}")
        return None

    chunks = semantic_chunker(text)
    result = hybrid_extract(chunks, use_llm=True)
    result["source_file"] = file_path.name
    return result

def merge_results(results):
    """Combine extracted dictionaries from multiple files."""
    merged = {}
    for r in results:
        for k, v in r.items():
            if not v:
                continue
            if k not in merged:
                merged[k] = v
            else:
                # Merge multiple values cleanly
                if merged[k] != v:
                    if not isinstance(merged[k], list):
                        merged[k] = [merged[k]]
                    if v not in merged[k]:
                        merged[k].append(v)
    return merged

def run_pipeline():
    """Process all bid folders and output consolidated JSON per bid."""
    base = Path(__file__).resolve().parents[2]
    raw_root = base / "data" / "raw_documents"
    output_root = base / "outputs"
    output_root.mkdir(exist_ok=True)

    bid_folders = [f for f in raw_root.iterdir() if f.is_dir()]
    print(f"Found {len(bid_folders)} bid folders")

    for bid_folder in bid_folders:
        print(f"\n🏗️ Processing folder: {bid_folder.name}")
        all_results = []

        for file in bid_folder.rglob("*"):
            if not file.suffix.lower() in [".pdf", ".html", ".htm", ".docx", ".txt"]:
                continue
            print(f"{file.name}")
            try:
                extracted = process_single_file(file)
                if extracted:
                    all_results.append(extracted)
            except Exception as e:
                print(f"Error processing {file.name}: {e}")

        # Merge and save consolidated JSON
        if all_results:
            merged_data = merge_results(all_results)
            out_path = output_root / f"{bid_folder.name}_consolidated.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(merged_data, f, indent=2)
            print(f"Consolidated JSON saved: {out_path}")
        else:
            print(f" No valid files found in {bid_folder.name}")

if __name__ == "__main__":
    run_pipeline()
