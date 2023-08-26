from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import db
from ..schemas import ContactCreate, ContactUpdate, ContactResponse, ContactListResponse, ContactSearchResponse
from ..database.models import Contact


router = APIRouter()


@router.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(db.get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.get("/contacts/", response_model=List[ContactListResponse])
def get_all_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(db.get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(db.get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(db.get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted"}


@router.get("/contacts/search/", response_model=List[ContactSearchResponse])
def search_contacts(query: Optional[str] = None, db: Session = Depends(db.get_db)):
    if query:
        contacts = db.query(Contact).filter(
            Contact.first_name.ilike(f"%{query}%") |
            Contact.last_name.ilike(f"%{query}%") |
            Contact.email.ilike(f"%{query}%")
        ).all()
    else:
        contacts = db.query(Contact).all()
    return contacts


@router.get("/contacts/birthday/", response_model=List[ContactSearchResponse])
def upcoming_birthdays(db: Session = Depends(db.get_db)):
    today = datetime.now()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        Contact.birthday >= today.date(),
        Contact.birthday <= next_week.date()
    ).all()
    return contacts

@router.get("/contacts/search/", response_model=List[ContactSearchResponse])
def search_contacts(query: Optional[str] = None, db: Session = Depends(db.get_db)):
    if query:
        contacts = db.query(Contact).filter(
            Contact.first_name.ilike(f"%{query}%") |
            Contact.last_name.ilike(f"%{query}%") |
            Contact.email.ilike(f"%{query}%")
        ).all()
    else:
        contacts = db.query(Contact).all()
    return contacts
