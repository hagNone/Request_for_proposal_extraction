import os, json
import google.generativeai as genai

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
        import re
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        json_text = json_match.group(0) if json_match else "{}"
        data = json.loads(json_text)
        return data
    except Exception as e:
        print("⚠️ Gemini extraction failed:", e)
        return {}



# 

"""
w-05-06', 'models/gemini-2.5-pro-preview-06-05', 'models/gemini-2.5-pro', 'models/gemini-2.0-flash-exp',
 'models/gemini-2.0-flash', 'models/gemini-2.0-flash-001', 'models/gemini-2.0-flash-exp-image-generation', 
 'models/gemini-2.0-flash-lite-001', 'models/gemini-2.0-flash-lite', 'models/gemini-2.0-flash-preview-image-generation', 
 'models/gemini-2.0-flash-lite-preview-02-05', 'models/gemini-2.0-flash-lite-preview', 'models/gemini-2.0-pro-exp',
   'models/gemini-2.0-pro-exp-02-05', 'models/gemini-exp-1206', 'models/gemini-2.0-flash-thinking-exp-01-21',
     'models/gemini-2.0-flash-thinking-exp', 'models/gemini-2.0-flash-thinking-exp-1219', 'models/gemini-2.5-flash-preview-tts', 
     'models/gemini-2.5-pro-preview-tts', 'models/learnlm-2.0-flash-experimental', 'models/gemma-3-1b-it', 'models/gemma-3-4b-it',
       'models/gemma-3-12b-it', 'models/gemma-3-27b-it', 'models/gemma-3n-e4b-it', 'models/gemma-3n-e2b-it',
         'models/gemini-flash-latest', 'models/gemini-flash-lite-latest', 'models/gemini-pro-latest',
           'models/gemini-2.5-flash-lite', 'models/gemini-2.5-flash-image-preview', 'models/gemini-2.5-flash-image', 
           'models/gemini-2.5-flash-preview-09-2025', 'models/gemini-2.5-flash-lite-preview-09-2025', 
           'models/gemini-robotics-er-1.5-preview', 'models/gemini-2.5-computer-use-preview-10-2025']"""