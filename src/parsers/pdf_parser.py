import pdfplumber
from bs4 import BeautifulSoup
from docx import Document
import re

def parse_pdf(path: str) -> str:
    """Extract readable text from a PDF."""
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)

def parse_html(path: str) -> str:
    """Extract visible text from HTML using BeautifulSoup."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    return text

def parse_docx(path: str) -> str:
    """Extract text from DOCX."""
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def parse_txt(path: str) -> str:
    """Read plain-text file."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def parse_document(path):
    """Auto-detect file type and route to parser."""
    path = str(path)  # Convert WindowsPath → string
    p = path.lower()

    if p.endswith(".pdf"):
        text = parse_pdf(path)
    elif p.endswith((".html", ".htm")):
        text = parse_html(path)
    elif p.endswith(".docx"):
        text = parse_docx(path)
    elif p.endswith(".txt"):
        text = parse_txt(path)
    else:
        raise ValueError(f"Unsupported file type: {path}")

    return clean_text(text)


# --- quick cleanup helpers ---
def clean_text(text: str) -> str:
    """Remove headers, page numbers, and redundant whitespace."""
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()
