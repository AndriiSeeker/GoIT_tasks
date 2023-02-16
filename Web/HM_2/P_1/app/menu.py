from app.Address_book.AdressBook import address_Book
from app.Sorter.sort import sort
from app.Notebook.notes import notepad
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import HTML, prompt


def bot(u_input):
    if u_input == "1":
        address_Book()

    if u_input == "2":
        while True:
            print(
                "Enter Directory to sort \nIn the format C:\ folder\....\ folder to sort \nOr 'exit' to exit"
            )
            u_input = input()
            if u_input in [".", "exit"]:
                break
            try:
                sort(u_input)
            except FileNotFoundError:
                print("There is no such directory, try again")
    if u_input == "3":
        notepad()


def main():
    while True:
        print(HTML("<ansigreen>Choose what you want to use:</ansigreen>"))
        print("1) Address book \n2) sorter \n3) Notepad")
        u_input = input(">>>").lower()
        bot(u_input)
        if u_input in [".", "exit"]:
            print(HTML("<ansired>Good bye!</ansired>"))
            break


if __name__ == "__main__":
    main()
