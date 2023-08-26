from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import db
from ..database.models import User

router = APIRouter()

@router.post("/verify/")
def verify_email(token: str):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.verified = True
    db.commit()
    
    return {"message": "Email verified successfully"}
