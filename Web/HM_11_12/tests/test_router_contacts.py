import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.database.models import User
from src.database.db import get_db
from main import app
from src.repository import contacts as rep_contacts
from src.services.auth import auth_service

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    db = next(get_db())
    yield db
    db.close()


@pytest.fixture
def authenticated_user(db_session):
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    yield user


@pytest.fixture
def test_contact(db_session, authenticated_user):
    contact = rep_contacts.create(
        {"name": "John Doe", "email": "johndoe@example.com"},
        authenticated_user,
        db_session,
    )
    yield contact
    rep_contacts.remove(contact.id, authenticated_user, db_session)


def test_get_contacts(authenticated_user, db_session):
    response = client.get(
        "/contacts/",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_get_contact_by_id(authenticated_user, db_session, test_contact):
    response = client.get(
        f"/contacts/{test_contact.id}",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "John Doe"


def test_get_contact_by_id_not_found(authenticated_user, db_session):
    response = client.get(
        "/contacts/123",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_contact_by_name(authenticated_user, db_session, test_contact):
    response = client.get(
        f"/contacts/names/John Doe",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "johndoe@example.com"


def test_get_contact_by_name_not_found(authenticated_user, db_session):
    response = client.get(
        "/contacts/names/John",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_contact_by_surname(authenticated_user, db_session, test_contact):
    response = client.get(
        f"/contacts/surnames/Doe",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "John Doe"


def test_get_contact_by_surname_not_found(authenticated_user, db_session):
    response = client.get(
        "/contacts/surnames/Smith",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_contact_by_email(authenticated_user, db_session, test_contact):
    response = client.get(
        f"/contacts/emails/johndoe@example.com",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "John Doe"


def test_get_contact_by_email_not_found(authenticated_user, db_session):
    response = client.get(
        "/contacts/emails/john@example.com",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_next_birth(authenticated_user, db_session):
    response = client.get(
        "/contacts/next_week/birthdays",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_owner(authenticated_user, db_session):
    data = {"name": "John Doe", "email": "johndoe@example.com"}
    response = client.post(
        "/contacts/",
        json=data,
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "John Doe"


def test_create_owner_conflict(authenticated_user, db_session, test_contact):
    data = {"name": "John Doe", "email": "johndoe@example.com"}
    response = client.post(
        "/contacts/",
        json=data,
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_contact(authenticated_user, db_session, test_contact):
    data = {"name": "John Smith"}
    response = client.put(
        f"/contacts/{test_contact.id}",
        json=data,
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "John Smith"


def test_update_contact_not_found(authenticated_user, db_session):
    data = {"name": "John Smith"}
    response = client.put(
        "/contacts/123",
        json=data,
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_remove_note(authenticated_user, db_session, test_contact):
    response = client.delete(
        f"/contacts/{test_contact.id}",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "John Doe"


def test_remove_note_not_found(authenticated_user, db_session):
    response = client.delete(
        "/contacts/123",
        headers={"Authorization": f"Bearer {authenticated_user.token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
