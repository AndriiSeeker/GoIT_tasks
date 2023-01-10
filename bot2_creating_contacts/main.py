from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, _value):
        self.value = _value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        value = value.replace("(", '')
        value = value.replace(")", '')
        value = value.replace("-", '')
        if value.isdigit() and value.startswith("+"):
            self.__value = value
        elif value.isdigit():
            self.__value = "+38" + value
        else:
            raise Exception("Sorry, the number was entered incorrectly")


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    # correct date = "2022-12-27" (year, month, date)

    @value.setter
    def value(self, value) -> None:
        if value:
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        self.__value = value


class Record:
    def __init__(self, name: Name, phone: Phone, birthday: Birthday):
        self.name = name
        self.list_phones = []
        self.birthday = birthday
        if phone is not None:
            self.list_phones.append(phone)

    def add_phone(self, phone: Phone):
        self.list_phones.append(phone)

    def change_phone(self, phone: Phone):
        self.list_phones = phone

    def delete_phone(self, phone: Phone, new_phone: Phone):
        self.list_phones.remove(phone)
        self.list_phones.append(new_phone)

    def show_contacts(self):
        full_list = str(self.name) + ": " + str(self.list_phones[0])
        full_list = str(full_list)
        for number in self.list_phones[1:]:
            full_list += ", " + (str(Phone(number)))
        return full_list

    def days_to_birthday(self):
        if self.birthday:
            start = datetime.now().date()
            birthday_date = datetime.strptime(str(self.birthday), "%Y-%m-%d")
            end = datetime(year=start.year,
                       month=birthday_date.month,
                       day=birthday_date.day).date()
            count_days = (end - start).days
            if count_days < 0:
                count_days += 365
            return f'Days to {self.name} birthday: {count_days}'
        else:
            return 'Unknown birthday'

    def __repr__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([str(phone) for phone in self.list_phones])}' \
               f' - Birthday: {self.birthday} '


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def show_user(self):
        return (', '.join(str(val) for val in self.data.values()))

    def iterator(self):
        for record in self.data.values():
            yield f"User {record.name} - Phones: {', '.join([phone.value for phone in record.list_phones])}"\
               f" - Birthday: {record.birthday}"


if __name__ == '__main__':
    pass
