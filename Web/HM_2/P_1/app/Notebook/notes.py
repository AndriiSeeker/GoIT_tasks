from datetime import datetime
from .notesclass import Tag, Note, Notebook
import time
from .decorator import input_error
from prompt_toolkit.completion import NestedCompleter


notebook = Notebook()


# add note
@input_error
def add_note(*args):
    if not args:
        return "Add text of note after command"
    note = " ".join(str(p) for p in args)
    if len(note) > 1000:
        return "Number of symbol > 1000, must be less"
    else:
        note = Note(note)
        return notebook.add_note(note)


# редагування нотатки
@input_error
def edit_note(number):
    note_key = int(number)
    ch_note = notebook[note_key]
    user_input = input(f" Input new text >>")
    notebook[note_key] = Note(user_input)
    ch_note.change_note(user_input)
    print(ch_note)
    return "Ok"


# add tag to note. You need to know 'number'. You can do some shearch and see number
@input_error
def add_tags(number, *tags):
    results = []
    for tag in tags:
        tag = Tag(tag)
        results.append(notebook[int(number)].add_tag(tag))
    return ", ".join(results)


# delete note tag. You need to know 'number'. You can do some shearch and see number
@input_error
def del_tag(number, tag):
    ch_note = notebook[int(number)]
    res = ch_note.del_tag(Tag(tag))
    if res:
        return f"Tag {tag} delete successful."
    return f"Tag {tag} not found"


# delete note by number. You need to know 'number'. You can do some shearch and see number
@input_error
def del_note(number):
    number = int(number)
    return notebook.pop(number)


@input_error
def search_by_tag(tag):
    notes = notebook.search_by_tag(Tag(tag))
    if not notes:
        return "No notes found with this phrase"
    return "\n".join(repr(p) for p in notes)


@input_error
def search_by_text(word):
    notes = notebook.search_by_word_in_note(word)
    if not notes:
        return "No notes found with this phrase"
    return "\n".join(repr(p) for p in notes)


@input_error
def search_by_date(date):
    print("Date have to be in format %Y-%m-%d")
    date_for_search = datetime.strptime(date, "%Y-%m-%d")
    notes = notebook.search_by_date(date_for_search)
    if not notes:
        return "No notes found with this date"
    return "\n".join(repr(p) for p in notes)


# notes sorting for date
@input_error
def sort_by_date():
    pr = ""
    notes = notebook.sort_by_date()
    for p in notes:
        pr = pr + "\n" + p.note_date.strftime("%Y-%m-%d") + "|| " + repr(p)
    return pr


# notes sorting for first tag
@input_error
def sort_by_tag():
    pr = ""
    notes = notebook.sort_by_tag()
    for p in notes:
        if not p.tags:
            str_tag = "empty"
        else:
            str_tag = str(p.tags[0])
        pr = pr + "\n" + "{:<20}".format(str_tag) + "|| " + repr(p)
    return pr


# show all existing dates
@input_error
def show_all_dates():
    return notebook.show_all_dates()


# show all existing tags
@input_error
def show_all_tags():
    return repr(notebook.show_all_tags())


@input_error
def show_one_note(number):
    return f"Full information: {repr(notebook[int(number)])} \nOnly text: {str(notebook[int(number)])}"


# show all existing tags
@input_error
def show_all_notes():
    return f"Note: " + "\nNote: ".join(repr((notebook[key])) for key in notebook.keys())


@input_error
def save_notebook(path="notebook.txt"):
    save_status = notebook.serializer(path)
    return save_status


@input_error
def save_notebook_with_ques(path="notebook.txt"):
    user_input = input("Do you want to save notes? (y/n)>>>")
    if user_input not in ("y", "n"):
        return "Try once more"
    elif user_input == "y":
        save_status = notebook.serializer(path)
        return save_status
    else:
        return " "


@input_error
def load_notebook(path="notebook.txt"):
    return notebook.deserializer(path)


@input_error
def help(*args):
    print(
        "I know these commands: \nadd_note <note_text>, \nedit <note_number>, \nadd_tag <note_number> <tag or list of tags>,"
        "\ndel_note <note_number>, \ndel_tag <note_number> <tag>, \nsearch_tag <tag>, \nsearch_text <text>, \nsearch_date <date>,"
        "\nsort_by_date, \nsort_by_tag, \nshow_dates, \nshow_tags,  \nshow_notes, \nshow_single, \nsave, \nhelp"
    )
    return " "


completer = NestedCompleter.from_nested_dict(
    {
        "add_note": None,
        "add_tag": None,
        "edit": None,
        "del_tag": None,
        "del_note": None,
        "search_tag": None,
        "search_text": None,
        "search_date": None,
        "sort_by_date": None,
        "sort_by_tag": None,
        "show_dates": None,
        "show_tags": None,
        "show_notes": None,
        "exit": None,
        "show_single": None,
        "save": None,
        "help": None,
    }
)

COMMANDS = {
    "add_note": add_note,
    "edit": edit_note,
    "add_tag": add_tags,
    "del_tag": del_tag,
    "del_note": del_note,
    "search_tag": search_by_tag,
    "search_text": search_by_text,
    "search_date": search_by_date,
    "sort_by_date": sort_by_date,
    "sort_by_tag": sort_by_tag,
    "show_dates": show_all_dates,
    "show_tags": show_all_tags,
    "show_notes": show_all_notes,
    "show_single": show_one_note,
    "save": save_notebook,
    "help": help,
}


def command_parser(user_input):
    key_word, *args = user_input.split()
    command = None
    key_word = key_word.lower()

    if key_word not in COMMANDS:
        return None, None
    command = COMMANDS.get(key_word)
    return command, *args


def notepad():
    print("Notebook is opened")

    load_status = load_notebook("notebook.txt")
    print(load_status)

    while True:
        u_input = input(">>>")
        u_input = u_input.lower()
        if u_input in [
            ".",
            "good bye",
            "close",
            "exit",
            "/",
        ]:
            print(save_notebook_with_ques())
            print("Good bye!")
            time.sleep(1.5)
            break
        command, *data = command_parser(u_input)
        if not command:
            result = "Enter command or choose 'help'"
        else:
            result = command(*data)
        print(result)
