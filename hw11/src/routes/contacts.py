from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse], name='Get a list of all contacts or contacts filtered by query parameters such as first name, last name or email')
async def get_contact_by_params(skip: int = 0, limit: int = Query(default=10),
                              first_name: Optional[str] = Query(default=None),
                              last_name: Optional[str] = Query(default=None),
                              email: Optional[str] = Query(default=None),
                              db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contacts(skip, limit, first_name, last_name, email, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts with requested parameters not found")
    return contact


@router.get("/birthdays", response_model=list[ContactResponse], name='Get list of contacts with birthdays for the next 7 days')
async def get_birthdays(skip: int = 0, limit: int = Query(default=10), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_birthdays(skip, limit, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts with birthdays for the next 7 days not found")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, name='Get contact by id')
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact with requested id not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    new_contact = await repository_contacts.create_contact(body, db)
    return new_contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact with requested id not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tag(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact with requested id not found")
    return contact
