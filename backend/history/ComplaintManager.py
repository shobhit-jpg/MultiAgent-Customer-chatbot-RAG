from uuid import uuid4
from datetime import datetime, timezone
from backend.history.mongodb import mongodb
import secrets
import string

class ComplaintManager:

    def __init__(self):
        self.collection = mongodb.complaints
    
    def create_complaint(self, email: str, subject: str):
        
        existing = self.collection.find_one({
            "email": email,
            "status": "Open"
               })

        if existing:
            
            return {
                "success": False,
                "message": "You already have an open complaint.",
                "complaint_id": existing["complaint_id"]
            }

        self.alphabet = string.ascii_uppercase + string.digits
        complaint_id = "TM-" + "".join(
            secrets.choice(self.alphabet) for _ in range(6)
        )

        complaint = {
            "complaint_id": complaint_id,
            "email": email,
            "subject": subject,
            "status": "Open",
            "summary": [],
            "created_at": datetime.now(timezone.utc)
        }

        self.collection.insert_one(complaint)     
        return {
                "success": True,
                "message": "Complaint registered.",
                "complaint_id": complaint_id
            }

    def update_summary(self, complaint_id: str, summary: str):
        
        result = self.collection.update_one(
            {"complaint_id": complaint_id},
            {
                "$push": {
                    "summary": summary
                }
            }
        )
        return result.modified_count > 0
        

    def check_status(self, complaint_id: str):
        complaint = self.collection.find_one(
            {"complaint_id": complaint_id},
            {"_id": 0}
        )

        if complaint:
            return complaint["status"]

        return "Complaint not found"
    
