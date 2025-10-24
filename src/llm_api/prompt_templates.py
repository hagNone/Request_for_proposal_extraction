import os, json
import google.generativeai as genai
import re

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

TARGET_FIELDS = [
    "Bid Number", "Title", "Due Date", "Bid Submission Type", "Term of Bid",
    "Pre Bid Meeting", "Installation", "Bid Bond Requirement", "Delivery Date",
    "Payment Terms", "Any Additional Documentation Required", "MFG for Registration",
    "Contract or Cooperative to use", "Model_no", "Part_no", "Product",
    "contact_info", "company_name", "Bid Summary", "Product Specification"
]

PROMPT = """
You are an expert in government RFP interpretation.
Extract the following fields from the given text and return a valid JSON object with these keys:
{fields}
If any information is missing, output null. Be concise and avoid unrelated text.
Text:
{text}
"""

def call_gemini_extract(chunks, existing_results):
    """Call Gemini to infer missing contextual fields."""
    text = " ".join([c["text"] for c in chunks[:6]])
    field_list = ", ".join(TARGET_FIELDS)
    prompt = PROMPT.format(fields=field_list, text=text)

    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)
        content = response.text.strip()
        # Try to isolate JSON
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        json_text = json_match.group(0) if json_match else "{}"
        data = json.loads(json_text)
        return data
    except Exception as e:
        print("Gemini extraction failed:", e)
        return {}



# 

