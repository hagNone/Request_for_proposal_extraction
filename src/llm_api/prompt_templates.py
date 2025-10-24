import os
import json
import re
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define schema fields in the required order
FIELDS = [
    "Bid Number",
    "Title",
    "Due Date",
    "Bid Submission Type",
    "Term of Bid",
    "Pre Bid Meeting",
    "Installation",
    "Bid Bond Requirement",
    "Delivery Date",
    "Payment Terms",
    "Any Additional Documentation Required",
    "MFG for Registration",
    "Contract or Cooperative to use",
    "Model_no",
    "Part_no",
    "Product",
    "contact_info",
    "company_name",
    "Bid Summary",
    "Product Specification"
]

# Gemini prompt template enforcing strict JSON output
PROMPT_TEMPLATE = """
You are an expert data extractor for RFP and Bid documents.

Your task:
Read the provided text carefully and extract **exactly** the following 20 fields.
You must ALWAYS include all 20 fields in your JSON output, in the same order shown.

If a field is missing, set its value to null.

Fields:
{fields}

Rules:
1. Return ONLY valid JSON — no explanations or commentary.
2. Use concise factual values, not full sentences.
3. If multiple values exist, return the most specific one.
4. Maintain the same field order.
5. Dates must be normalized as "YYYY-MM-DD HH:MM" if possible.
6. Never invent data.
7. Ensure all fields exist in the JSON output, even if null.

Example Output Format:
{{
  "Bid Number": "JA-207652",
  "Title": "Student and Staff Computing Devices",
  "Due Date": "2024-07-09 14:00",
  "Bid Submission Type": "Electronic",
  "Term of Bid": "Three years with two renewals",
  "Pre Bid Meeting": "2024-06-10 15:00 via Teams",
  "Installation": "Yes, includes delivery & setup",
  "Bid Bond Requirement": null,
  "Delivery Date": "2024-09-01",
  "Payment Terms": "Net 30 Days",
  "Any Additional Documentation Required": "Signed Addenda, Warranty Certificates",
  "MFG for Registration": "Dell",
  "Contract or Cooperative to use": "Dallas ISD Local Contract",
  "Model_no": "Latitude 5550",
  "Part_no": "CC7802",
  "Product": "Dell Latitude 5550 Laptops",
  "contact_info": "ProcurementCS@dallasisd.org, 972-925-3700",
  "company_name": "Dallas Independent School District",
  "Bid Summary": "Procurement for student computing devices and accessories.",
  "Product Specification": "Intel i5, 16GB RAM, 256GB SSD, Windows 11 Pro"
}}

Now extract all 20 fields for the following text:
{text}
"""

def call_gemini_extract(chunks, existing_results=None):
    """Use Gemini to extract all 20 fields in strict schema order."""
    full_text = " ".join([c["text"] for c in chunks[:8]])  # combine top chunks
    field_list = "\n".join([f"{i+1}. {f}" for i, f in enumerate(FIELDS)])
    prompt = PROMPT_TEMPLATE.format(fields=field_list, text=full_text)

    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)
        content = (response.text or "").strip()

        # Extract JSON safely
        match = re.search(r"\{[\s\S]*\}", content)
        json_text = match.group(0) if match else "{}"

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            json_text = json_text.replace("'", '"')
            json_text = re.sub(r",\s*([\]}])", r"\1", json_text)
            data = json.loads(json_text) if json_text else {}

        # Ensure all fields are present
        for f in FIELDS:
            data.setdefault(f, None)

        print("Gemini extraction complete (strict schema).")
        return data

    except Exception as e:
        print("Gemini extraction failed:", e)
        return {f: None for f in FIELDS}
