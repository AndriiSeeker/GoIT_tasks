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
    """
    The get_contacts function returns a list of contacts for the given user.

    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """

    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def find_contact_by_id(id: int, user: User, db: Session):
    """
    The find_contact_by_id function takes in an id and a user, and returns the contact with that id.
        Args:
            id (int): The ID of the contact to find.
            user (User): The User object for which we are finding contacts.

    :param id: int: Find the contact by id
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass a database session to the function
    :return: The contact with the given id
    """

    contact = db.query(Contact).filter(and_(Contact.id == id, Contact.user_id == user.id)).first()
    return contact


async def find_contact_by_name(name: str, user: User, db: Session):
    """
    The find_contact_by_name function takes in a name and user, and returns the contact with that name.
        Args:
            name (str): The contact's first.
            user (User): The current logged-in User object.

    :param name: str: Specify the name of the contact we are looking for
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """

    contact = db.query(Contact).filter(and_(Contact.name == name, Contact.user_id == user.id)).first()
    return contact


async def find_contact_by_surname(surname: str, user: User, db: Session):
    """
    The find_contact_by_surname function takes in a surname and returns the contact with that surname.
        Args:
            surname (str): The last name of the contact to be found.
            user (User): The user who owns the contacts being searched through.

    :param surname: str: Pass in the surname of the contact we want to find
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A contact with a surname that matches the input parameter
    """

    contact = db.query(Contact).filter(and_(Contact.surname == surname, Contact.user_id == user.id)).first()
    return contact


async def find_contact_by_email(email: EmailStr, user: User, db: Session):
    """
    The find_contact_by_email function takes in an email address and a user object,
    and returns the contact associated with that email address. If no such contact exists,
    it returns None.

    :param email: EmailStr: Specify the email address of the contact to be found
    :param user: User: Identify the user that is making the request
    :param db: Session: Access the database
    :return: The first contact with a given email address
    """

    contact = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).first()
    return contact


async def next_week_birthdays(user: User, db: Session):
    """
    The next_week_birthdays function returns a list of contacts whose birthdays are in the next week.
        Args:
            user (User): The user who is requesting the information.
            db (Session): A database session to query for data.

    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts whose birthdays are in the next week
    """

    result_contacts = []
    start = datetime.now()
    end = start + timedelta(days=7)
    year = start.year
    start_month = start.month
    end_month = end.month
    contacts_list = []
    contacts_list_ = db.query(Contact).filter(Contact.user_id == user.id).all()
    for obj in contacts_list_:
        if obj.birth.month == start_month:
            contacts_list.append(obj)
    if end_month != start_month:
        contacts_list.extend(db.query(Contact).filter(extract('month', Contact.birth) == end_month).all())
    for contact in contacts_list:
        birthday = contact.birth
        birthday = birthday.replace(year=year)
        if start <= birthday < end:
            result_contacts.append(contact)
    return result_contacts


async def create(body: ContactModel, user: User, db: Session):
    """
    The create function creates a new contact in the database.

    :param body: ContactModel: Create a new contact
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The created contact
    """

    contact = Contact(**body.dict(), user_id=user.id)  # Owner(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated version of the ContactModel object.

    :param contact_id: int: Identify the contact that is to be deleted
    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The contact that was updated
    """

    contact = await find_contact_by_id(contact_id, user, db)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.birth = body.birth
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    """
    The remove function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to remove.
            user (User): The user who is removing the contact.
            db (Session): A connection to our database.

    :param contact_id: int: Find the contact in the database
    :param user: User: Identify the user that is making the request
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed
    """

    contact = await find_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
