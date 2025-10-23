from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class RFPDocument(BaseModel):
    Bid_Number: Optional[str] = Field(None, alias="Bid Number")
    Title: Optional[str] = None
    Due_Date: Optional[str] = None
    Bid_Submission_Type: Optional[str] = None
    Term_of_Bid: Optional[str] = None
    Pre_Bid_Meeting: Optional[str] = None
    Installation: Optional[str] = None
    Bid_Bond_Requirement: Optional[str] = None
    Delivery_Date: Optional[str] = None
    Payment_Terms: Optional[str] = None
    Additional_Documentation_Required: Optional[str] = None
    MFG_for_Registration: Optional[str] = None
    Contract_or_Cooperative_to_use: Optional[str] = None
    Model_no: Optional[str] = None
    Part_no: Optional[str] = None
    Product: Optional[str] = None
    Contact_Info: Optional[str] = None
    Company_Name: Optional[str] = None
    Bid_Summary: Optional[str] = None
    Product_Specification: Optional[str] = None
    Additional_Metadata: Optional[Dict[str, str]] = None
