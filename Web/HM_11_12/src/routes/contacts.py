from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import ContactResponse, ContactModel
from src.database.db import get_db
from src.repository import contacts as rep_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await rep_contacts.get_contacts(current_user, db)
    return contacts


@router.get("/{id}", response_model=ContactResponse)
async def get_contact_by_id(id: int = Path(ge=1), db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.find_contact_by_id(id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/names/{name}", response_model=ContactResponse)
async def get_contact_by_name(name: str = Path(), db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.find_contact_by_name(name, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/surnames/{surname}", response_model=ContactResponse)
async def get_contact_by_surname(surname, db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.find_contact_by_surname(surname, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/emails/{email}", response_model=ContactResponse)
async def get_contact_by_email(email: EmailStr = Path(), db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.find_contact_by_email(email, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.get("/next_week/birthdays", response_model=List[ContactResponse])
async def get_next_birth(db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.next_week_birthdays(current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_owner(body: ContactModel, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.find_contact_by_name(body.name, current_user, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is exists!")
    contact = await rep_contacts.create(body, current_user, db)
    return contact


@router.put("/{id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, id: int = Path(), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.update(id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.delete("/{id}", response_model=ContactResponse)
async def remove_note(id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await rep_contacts.remove(id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact