from datetime import datetime, timedelta
from typing import List

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import extract, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.services.auth import auth_service


async def get_contacts(user: User, db: Session) -> List[Contact]:
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def find_contact_by_id(id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == id, Contact.user_id == user.id)).first()
    return contact


async def find_contact_by_name(name: str, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).first()
    return contact


async def find_contact_by_surname(surname: str, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).first()
    return contact


async def find_contact_by_email(email: EmailStr, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).first()
    return contact


async def next_week_birthdays(user: User, db: Session):
    result_contacts = []
    start = datetime.now()
    end = start + timedelta(days=7)
    year = start.year
    start_month = start.month
    end_month = end.month
    contacts_list = []
    contacts_list_ = db.query(Contact).filter(Contact.user_id == user.id).all()
    print(contacts_list_)
    for obj in contacts_list_:
        if obj.birth.month == start_month:
            contacts_list.append(obj)
    print(contacts_list)
    if end_month != start_month:
        contacts_list.extend(db.query(Contact).filter(extract('month', Contact.birth) == end_month).all())
    for contact in contacts_list:
        birthday = contact.birth
        birthday = birthday.replace(year=year)
        if start <= birthday < end:
            result_contacts.append(contact)
    return result_contacts


async def create(body: ContactModel, user: User, db: Session):
    contact = Contact(**body.dict(), user_id=user.id)  # Owner(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    contact = await find_contact_by_id(contact_id, user, db)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.birth = body.birth
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    contact = await find_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
