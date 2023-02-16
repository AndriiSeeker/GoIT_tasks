from collections import UserDict

# from Class import *
from .Class import *
from datetime import datetime
from prompt_toolkit import print_formatted_text, prompt, HTML
from prompt_toolkit.completion import NestedCompleter
import pickle

try:
    with open("AddressBook.bin", "rb") as file:
        ab = pickle.load(file)
except:
    ab = AddressBook()
pages = []


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            print("Sorry, try again")
        except ValueError:
            print("incorrect input")
        except KeyError:
            print("incorrect Name")
        except AttributeError:
            print("incorrect Email")

    return wrapper


def greetings(*args):
    print("How can I help you?")


def help(*args):
    print(
        "I know these commands:  hello, add, append, change, phone, show, del_phon, birthday, day, page, search,  email, home, happy_birthday, help"
    )


@input_error
def add(*argv):
    phone, birthday = None, None
    name = Name(argv[0][0])
    if len(argv[0]) >= 2:
        phone = Phone(argv[0][1])
    if len(argv[0]) >= 3:
        birthday = Birthday(argv[0][2])
    ab.add_record(Record(name, phone, birthday))
    print(f"Contact {name} added")


@input_error
def add_phon(*argv):
    ab[argv[0][0].title()].add_phone(Phone(argv[0][1]))
    print(f"phone {argv[0][1]} added to contact {argv[0][0].title()}")


@input_error
def change(*argv):
    if len(argv[0]) == 3:
        ab[argv[0][0].title()].add_phone(Phone(argv[0][2]))
        ab[argv[0][0].title()].delete_phone(Phone(argv[0][1]))
        print(
            f"In contact {argv[0][0].title()} number {argv[0][1]} is replaced by {argv[0][2]}"
        )
    else:
        print(
            "To change the number, enter the name of the contact, the number to change, the new phone number"
        )


@input_error
def del_phone(*argv):
    ab[argv[0][0].title()].delete_phone(Phone(argv[0][1]))
    print(f"Phone {argv[0][1]} removed from contact {argv[0][0].title()}")


@input_error
def show_all(*argv):
    print(ab)


@input_error
def page(*argv):
    reg = ab.iteration(2)
    for b in reg:
        pages.append(b)
    print(f"page {int(argv[0][0])} of {len(pages)}")
    for i in pages[int(argv[0][0]) - 1]:
        print(i[1])


@input_error
def output_phone(name):
    print(ab[name[0].title()])
    if ab[name[0].title()].birthday:
        print(f"Birthday: {ab[name[0].title()].birthday}")
    if ab[name[0].title()].email:
        print(f"email: {ab[name[0].title()].email}")
    if ab[name[0].title()].address:
        print(f"address: {ab[name[0].title()].address}")


@input_error
def add_birthday(*args):
    ab[args[0][0].title()].birthday = Birthday(args[0][1])
    print(f"Birthday {args[0][1]} added to contact {args[0][0].title()}")


@input_error
def search(val):
    if val[0].isdigit():
        for p in ab.items():
            for x in p[1].phones:
                if not str(x).find(val[0]) == -1:
                    print(p[1])
    else:
        for p in ab.items():
            if not p[0].lower().find(val[0].lower()) == -1:
                print(p[1])


@input_error
def day_birthday(name):
    print(f"Before birthday {name[0].title()}, {ab[name[0].title()].days_to_bd()} days")


@input_error
def add_email(*args):
    ab[args[0][0].title()].email = Email(args[0][1])
    print(f"Email {args[0][1]} added to contact {args[0][0].title()}")


@input_error
def add_address(*args):
    ab[args[0][0].title()].address = Address(args[0][1])
    print(f"Address {args[0][1]} added to contact {args[0][0].title()}")


@input_error
def birthday_ib_day(day):
    print(f"In {day[0]} days the birthday of:")
    ab.birthday_ib_day(int(day[0]))


completer = NestedCompleter.from_nested_dict(
    {
        "hello": None,
        "add": None,
        "append": None,
        "change": None,
        "phone": None,
        "show": None,
        "del": None,
        "birthday": None,
        "day": None,
        "page": None,
        "search": None,
        "email": None,
        "happy_birthday": None,
        "exit": None,
        "home": None,
    }
)

COMMANDS = {
    greetings: "hello",
    add: "add",
    add_phon: "append",
    change: "change",
    output_phone: "phone",
    show_all: "show",
    del_phone: "del_phon",
    add_birthday: "birthday",
    day_birthday: "day",
    page: "page",
    search: "search",
    add_email: "email",
    add_address: "home",
    help: "help",
    birthday_ib_day: "happy_birthday",
}


def command_parser(u_input: str):
    for comand, key_words in COMMANDS.items():
        if u_input.startswith(key_words):
            return comand, u_input.replace(key_words, "").strip().split(" ")
    return None, None


def address_Book():
    print("Address book open")

    while True:
        u_input = prompt(">>>", completer=completer)
        u_input = u_input.lower()
        if u_input in [".", "good bye", "close", "exit", "/", ""]:
            print("Good bye!")
            break
        comand, data = command_parser(u_input)
        if not comand:
            print("Enter command")
        else:
            comand(data)

    with open("AddressBook.bin", "wb") as file:
        pickle.dump(ab, file)


if __name__ == "__main__":
    address_Book()
