from collections import UserDict
from datetime import datetime, timedelta
from itertools import islice
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"


class Birthday(Field):
    # (рік-місяць-день)
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: str):
        data = val.split("-")
        if not "".join(data).isdigit():
            raise ValueError
        if int(data[0]) > datetime.now().year or int(data[1]) > 12 or int(data[2]) > 30:
            raise ValueError
        self.__value = val


class Address(Field):
    def __init__(self, value):
        self.value = value


class Email(Field):
    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            result = None
            get_email = re.findall(r"\b[a-zA-Z][\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}", value)
            if get_email:
                for e in get_email:
                    result = e
            if result is None:
                raise AttributeError(f"Incorrect value provided {value}")
            self.__value = result


class Name(Field):
    def __init__(self, value):
        self.value = value.capitalize()


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: str):
        if not len(val) == 10 and not len(val) == 13 and not val.lstrip("+").isdigit():
            raise ValueError
        if len(val) == 10:
            val = "+38" + val
        if not val[3] == "0":
            raise ValueError
        self.__value = val


class Record:
    def __init__(
        self,
        name: Name,
        phone: Phone = None,
        birthday: Birthday = None,
        email=None,
        address: Address = None,
    ):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.address = address
        if phone:
            self.phones.append(phone)

    def __str__(self):
        return f"{self.name} - {', '.join([str(p) for p in self.phones])}"

    def __repr__(self):
        return f"{self.name} - {', '.join([str(p) for p in self.phones])}"

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def delete_phone(self, phone: Phone):
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return f"Phone {p.value} delete successful."
        return f"Phone {phone.value} not found"

    def days_to_bd(self):
        # (рік-місяць-день)
        if not self.birthday:
            print("Birthday not entered")
        else:
            date1 = self.birthday.value.split("-")
            date = datetime(
                year=datetime.now().year, month=int(date1[1]), day=int(date1[2])
            )
            data_now = datetime.now()
            dat = date - data_now
            return dat.days

    def add_email(self, email):
        self.email = email

    def add_address(self, address):
        self.address = address

    def add_birthday(self, birthday):
        self.birthday = birthday


class AddressBook(UserDict):
    index = 0

    def add_record(self, rec: Record):
        self[rec.name.value] = rec

    def __str__(self):
        return "\n".join([str(i) for i in self.values()])

    def iteration(self, step=5):
        while AddressBook.index < len(self):
            yield list(
                islice(self.items(), AddressBook.index, AddressBook.index + step)
            )
            if AddressBook.index > len(self):
                raise StopIteration()
            AddressBook.index += step

    def birthday_ib_day(self, day):
        days = datetime.now().date() + timedelta(days=day)
        caunt = 0
        for i in self:
            if self[i].birthday:
                date1 = self[i].birthday.value.split("-")
                date = datetime(
                    year=datetime.now().year, month=int(date1[1]), day=int(date1[2])
                ).date()
                if days == date:
                    print(self[i])
                    caunt += 1
        if caunt == 0:
            print(f"In {day} days there is no birthday")


if __name__ == "__main__":
    name = Name("Bill")
    phone = Phone("0666266830")
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)
    name1 = Name("alisa")
    phone1 = Phone("+380662951095")
    rec1 = Record(name1, phone1)
    rec1.add_birthday(Birthday("1997-02-01"))
    ab.add_record(rec1)
    ab.birthday_ib_day(1)
