import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def semantic_chunker(text: str, chunk_size: int = 1500, chunk_overlap: int = 100):
    """
    Split cleaned RFP text into logical chunks.
    We first separate major sections, then break long ones into ~1500-character pieces.
    """

    # split on section-like headings 
    sections = re.split(
        r'(?i)(SECTION\s+\d+|SCOPE|SPECIFICATION|TERMS|ADDENDUM|REQUIREMENTS)',
        text,
    )

    # keep only meaningful text blocks 
    cleaned_sections = [s.strip() for s in sections if len(s.strip()) > 100]

    #further subdivide long blocks using LangChain splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    chunks = []
    for s in cleaned_sections:
        sub_chunks = splitter.split_text(s)
        for sub in sub_chunks:
            chunks.append({"text": sub})
    return chunks


# quick manual test when you run this file directly
if __name__ == "__main__":
    sample = """SECTION 1 – INTRODUCTION
    Dallas ISD Request for Proposal JA-207652 Student and Staff Computing Devices.
    Proposals due July 9, 2024 at 2:00 PM CST. SECTION 2 – TERMS AND CONDITIONS …"""
    pieces = semantic_chunker(sample)
    print(f"{len(pieces)} chunks created")
    print(pieces[0]["text"])
