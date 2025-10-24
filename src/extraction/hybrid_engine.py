import re
from src.llm_api.prompt_templates import call_gemini_extract

# Deterministic regex rules for quick fields
PATTERNS = {
    "Bid Number": re.compile(r"\b(?:RFP|BID|JA)[\s#:-]*\d{3,7}\b", re.I),
    "Due Date": re.compile(r"(?:Due|Closing|Submission)\s*(?:Date|Time)[:\s]*([A-Za-z0-9 ,:/-]+)", re.I),
    "contact_info": re.compile(r"[\w\.-]+@[\w\.-]+\.\w+|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", re.I),
    "company_name": re.compile(r"(?:Company\s*Name)[:\s]*([A-Za-z0-9 &.,'-]+)", re.I),
    "Title": re.compile(r"(?:Title|Solicitation)\s*[:\-]?\s*(.*)", re.I)
}

def apply_rule_extraction(text: str):
    """Return deterministic field matches."""
    results = {}
    for field, pattern in PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            results[field] = matches[0] if isinstance(matches, list) else matches
    return results


# Hybrid extractor combining regex + Gemini 
def hybrid_extract(chunks, use_llm=True):
    """
    Combine rule-based extraction and Gemini contextual extraction.
    """
    full_text = " ".join([c["text"] for c in chunks])
    rule_results = apply_rule_extraction(full_text)

    if use_llm:
        llm_results = call_gemini_extract(chunks, rule_results)
        rule_results.update({k: v for k, v in llm_results.items() if v})

    return rule_results


if __name__ == "__main__":
    # quick self-test
    sample_text = """
    RFP JA-207652 Student and Staff Computing Devices
    Proposals Due July 9, 2024 at 2:00 PM CST
    Dallas ISD ProcurementCS@dallasisd.org
    """
    fake_chunks = [{"text": sample_text}]
    print(hybrid_extract(fake_chunks, use_llm=False))
