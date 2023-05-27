from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import ContactResponse, ContactModel
from src.database.db import get_db
from src.repository import contacts as rep_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], description='No more than 20 requests per minute',
            dependencies=[Depends(RateLimiter(times=20, seconds=60))])
async def get_contacts(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function returns a list of contacts for the current user.

    :param db: Session: Get a database session
    :param current_user: User: Get the current user
    :return: A list of contacts
    """

    contacts = await rep_contacts.get_contacts(current_user, db)
    return contacts


@router.get("/{id}", response_model=ContactResponse)
async def get_contact_by_id(id: int = Path(ge=1), db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_id function is a GET request that returns the contact with the given id.
        The function takes in an id as a path parameter and uses it to find the contact in question.
        If no such contact exists, then an HTTP 404 error is returned.

    :param id: int: Specify the id of the contact to be returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is currently logged in
    :return: A contact object
    """

    contact = await rep_contacts.find_contact_by_id(id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/names/{name}", response_model=ContactResponse)
async def get_contact_by_name(name: str = Path(), db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_name function is a GET request that returns the contact with the given name.
        It takes in a name as an argument and uses it to find the contact with that name. If no such
        contact exists, then it raises an HTTPException.

    :param name: str: Get the name of the contact from the url
    :param db: Session: Get a database session
    :param current_user: User: Get the current user
    :return: A contact object with the given name
    """

    contact = await rep_contacts.find_contact_by_name(name, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/surnames/{surname}", response_model=ContactResponse)
async def get_contact_by_surname(surname, db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_surname function is a GET request that returns the contact with the given surname.
        If no such contact exists, it will return a 404 error.

    :param surname: Find the contact in the database
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """

    contact = await rep_contacts.find_contact_by_surname(surname, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/emails/{email}", response_model=ContactResponse)
async def get_contact_by_email(email: EmailStr = Path(), db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_email function is a GET request that returns the contact with the specified email.
    The function takes in an email as a parameter and uses it to find the contact in question. If no such
    contact exists, then an HTTPException is raised.

    :param email: EmailStr: Validate the email address
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    """

    contact = await rep_contacts.find_contact_by_email(email, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/next_week/birthdays", response_model=List[ContactResponse])
async def get_next_birth(db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_next_birth function returns the next birthday of a contact.
        The function is called by the /next_birth endpoint, which takes no parameters.
        It returns a JSON object containing information about the next birthday.

    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user id
    :return: A contact object with the next birthday
    """

    contact = await rep_contacts.next_week_birthdays(current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 5 requests per minute',
             dependencies=[Depends(RateLimiter(times=5, seconds=60))]
             )
async def create_owner(body: ContactModel, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_owner function creates a new owner in the database.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A contact model object
    """

    contact = await rep_contacts.find_contact_by_name(body.name, current_user, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is exists!")
    contact = await rep_contacts.create(body, current_user, db)
    return contact


@router.put("/{id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, id: int = Path(), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, which is then passed to the update method of the ContactRepository class.
        If no contact with that id exists, it raises an HTTPException with status code 404 (Not Found).

    :param body: ContactModel: Pass the contact data to the function
    :param id: int: Get the id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is currently logged in
    :return: The updated contact, or raises a 404 error if the note is not found
    """

    contact = await rep_contacts.update(id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.delete("/{id}", response_model=ContactResponse)
async def remove_note(id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_note function is used to remove a note from the database.
        The function takes in an id and a db, which are both required.
        The current_user is also required but it's not passed in as an argument,
        instead it's passed into the Depends() function which returns the user object.

    :param id: int: Identify the note to be removed
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the user that is currently logged in
    :return: The contact that was removed
    """

    contact = await rep_contacts.remove(id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact
