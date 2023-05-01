from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, first_name: str, last_name: str, email: str, db: Session):
    first_name_query = db.query(Contact).filter(Contact.first_name == first_name)
    last_name_query = db.query(Contact).filter(Contact.last_name == last_name)
    email_query = db.query(Contact).filter(Contact.email == email)
    if first_name and last_name and email:
        return first_name_query.union(last_name_query).union(email_query).all()
    if first_name and last_name:
        return first_name_query.union(last_name_query).all()
    if first_name and email:
        return first_name_query.union(email_query).all()
    if last_name and email:
        return last_name_query.union(email_query).all()
    if first_name:
        return first_name_query.all()
    if last_name:
        return last_name_query.all()
    if email:
        return email_query.all()
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contacts_birthdays(skip: int, limit: int, db: Session):
    contacts_with_birthdays = []
    today = date.today()
    current_year = today.year
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    for contact in contacts:
        td = contact.date_of_birth.replace(year=current_year) - today
        if 0 <= td.days <= 7:
            contacts_with_birthdays.append(contact)
        else:
            continue
    return contacts_with_birthdays


async def get_contact_by_id(contact_id: int, db: Session):
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(first_name = body.first_name, last_name = body.last_name, email = body.email, phone = body.phone, date_of_birth = body.date_of_birth)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact