import json
from src.schemas.rfp_schema import RFPDocument

def safe_first(value):
    if isinstance(value, list):
        return ", ".join([str(v) for v in value])
    return value

def validate_and_serialize(raw_dict):
    cleaned = {k: safe_first(v) for k, v in raw_dict.items()}
    doc = RFPDocument(**cleaned)
    return json.dumps(doc.dict(), indent=2)

