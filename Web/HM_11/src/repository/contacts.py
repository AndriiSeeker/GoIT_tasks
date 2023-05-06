from datetime import datetime, timedelta

from pydantic import EmailStr
from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def find_contact_by_id(id: int, db: Session):
    contact = db.query(Contact).filter_by(id=id).first()
    return contact


async def find_contact_by_name(name: str, db: Session):
    contact = db.query(Contact).filter(Contact.name == name).first()
    return contact


async def find_contact_by_surname(surname: str, db: Session):
    contact = db.query(Contact).filter(Contact.surname == surname).first()
    return contact


async def find_contact_by_email(email: EmailStr, db: Session):
    contact = db.query(Contact).filter(Contact.email == email).first()
    return contact


async def next_week_birthdays(db: Session):
    result_contacts = []
    start = datetime.now()
    end = start + timedelta(days=7)
    year = start.year
    start_month = start.month
    end_month = end.month
    contacts_list = db.query(Contact).filter(extract('month', Contact.birth) == start_month).all()
    if end_month != start_month:
        contacts_list.extend(db.query(Contact).filter(extract('month', Contact.birth) == end_month).all())
    for contact in contacts_list:
        birthday = contact.birth
        birthday = birthday.replace(year=year)
        if start <= birthday < end:
            result_contacts.append(contact)
    return result_contacts


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())  # Owner(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await find_contact_by_id(contact_id, db)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.birth = body.birth
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await find_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
