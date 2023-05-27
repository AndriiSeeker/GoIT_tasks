import unittest
import datetime
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.repository.contacts import get_contacts, create, find_contact_by_id, find_contact_by_name, \
    find_contact_by_surname, update

from src.schemas import ContactModel

'''repository/contacts'''


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username="seeker", email="aaa@gmail.com", password="QWERTY")

    async def test_get_contacts(self):
        contacts = [Contact() for _ in range(5)]
        self.session.query(Contact).filter().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_find_contact_by_id(self):
        contact = Contact()
        id = 1
        self.session.query(Contact).filter().first.return_value = contact
        result = await find_contact_by_id(id=id, user=self.user, db=self.session)
        self.assertEqual(result.id, contact.id)

    async def test_find_contact_by_name(self):
        contact = Contact()
        name = 'Andrii'
        self.session.query(Contact).filter().first.return_value = contact
        result = await find_contact_by_name(name=name, user=self.user, db=self.session)
        self.assertEqual(result.name, contact.name)

    async def test_find_contact_by_surname(self):
        contact = Contact()
        surname = 'Svitelskyi'
        self.session.query(Contact).filter().first.return_value = contact
        result = await find_contact_by_surname(surname=surname, user=self.user, db=self.session)
        self.assertEqual(result.surname, contact.surname)

    # async def test_next_week_birthdays(self):
    #     contact = Contact()
    #     surname = 'Svitelskyi'
    #     self.session.query(Contact).filter().first.return_value = contact
    #     result = await find_contact_by_surname(surname=surname, user=self.user, db=self.session)
    #     self.assertEqual(result.surname, contact.surname)

    # async def test_update(self):
    #     contact = await find_contact_by_id(id=1, user=self.user, db=self.session)
    #     if contact:
    #         contact.name = self.user.name
    #         contact.surname = self.user.surname
    #         contact.email = self.user.email
    #         contact.birth = self.user.birth
    #     result = await update(contact_id=1, body=contact, user=self.user, db=self.session)
    #     self.assertEqual(result, contact)

    async def test_create(self):
        body = ContactModel(id=2,
                            name="Vasya",
                            surname="Romanenko",
                            email="rom_vas@gmail.com",
                            phone="0502307099",
                            birth=datetime.date(year=2004, month=11, day=4),
                            description="Example"
                            )
        result = await create(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertTrue(hasattr(result, 'id'))


if __name__ == '__main__':
    unittest.main()
