from collections import UserDict
from datetime import datetime, date
import pickle
import re


# class Tags - key words, we add it to notes, as class Phones in home work, max lenght = 20
class Tag:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if len(value) > 20:
            raise ValueError("Max token length is 20 symbols")
        self.__value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if not other:
            return False
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value


# class Note. It has required field - title, text_content, optional field - tags
class Note:
    def __init__(self, text_content: str, *tag):
        self.text = text_content
        self.number = None
        self.tags = []
        self.note_date = datetime.today().date()
        for i in tag:
            self.tags.append(Tag(i))

    # add tag to note
    def add_tag(self, tag: Tag):
        if tag not in self.tags:
            return self.tags.append(tag)
        return self.tags

    # delete tag
    def del_tag(self, tag: Tag):
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    # replace one note to another
    def change_note(self, new_text):
        self.text = new_text
        return "Ok"

    # long representation. Note text cats to 50 symbols
    def __repr__(self):
        if len(self.text) < 50:
            text = self.text
        else:
            text = self.text[0:50] + "..."
        if not self.tags:
            tags = "empty"
        else:
            tags = self.show_all_tags()

        return (
            f"Number: {self.number}, Date: {self.note_date}, Tags: {tags}, Text: {text}"
        )

    # short representation. Only note text. If text > 50 - print line 50n symb
    def __str__(self):
        i = 0
        pr_str = ""
        pos_space = 0
        if len(self.text) < 50:
            return self.text
        else:
            while i < (len(self.text) - 50):
                pos_space = self.text[i : i + 50].rfind(" ")
                pr_str = pr_str + self.text[i : i + pos_space] + "\n"
                i += pos_space + 1
            if i < len(self.text):
                pr_str = pr_str + self.text[i:]
        return pr_str

    def show_all_tags(self):
        return ", ".join(str(p) for p in self.tags)


# class Notebook == Adressbook, dictionary, where key is unic class counter
class Notebook(UserDict):
    index = 0

    # add new note with class-count number as key
    def add_note(self, note: Note):
        Notebook.index += 1
        note.number = Notebook.index
        self.data[Notebook.index] = note
        return "note added"

    def search_by_tag(self, tag: Tag):
        note_list = []
        for value in self.data.values():
            if tag in value.tags:
                note_list.append(value)
        return note_list

    # to do search if we have some words in note text
    def search_by_word_in_note(self, phrase):
        text_coincidence = []
        for value in self.data.values():
            if re.search(phrase, value.text, flags=re.IGNORECASE):
                text_coincidence.append(value)
        return text_coincidence

    # to do search if we have date
    def search_by_date(self, day: date):
        date_list = []
        for value in self.data.values():
            if day.date() == value.note_date:
                date_list.append(value)

        return date_list

    # sort list of instances
    def sort_by_date(self):
        object_list = list(self.data.values())
        object_list.sort(key=lambda note: note.note_date)
        return object_list

    @staticmethod
    def sort_key_tag(note):
        if note.tags:
            return note.tags[0]
        else:
            return Tag("")

    # sort list of instances
    def sort_by_tag(self):
        object_list = list(self.data.values())
        object_list.sort(key=Notebook.sort_key_tag)
        return object_list

    @staticmethod
    def sort_key_tag(note):
        if note.tags:
            return note.tags[0]
        else:
            return Tag("")

    # sort list of instances
    def sort_by_tag(self):
        object_list = list(self.data.values())
        object_list.sort(key=Notebook.sort_key_tag)
        return object_list

    # show list of tags
    def show_all_tags(self):
        tags_list = []

        for value in self.data.values():
            for item in value.tags:
                if item not in tags_list:
                    tags_list.append(item)

        tags_list.sort()
        return tags_list

    # show all dates
    def show_all_dates(self):
        date_list = []
        for value in self.data.values():
            if value.note_date not in date_list:
                date_list.append(value.note_date)

        date_list.sort()
        return ", ".join(p.strftime("%Y-%m-%d") for p in date_list)

    # serialize Notebook
    def serializer(self, path_to_book):
        if not self.data:
            return "Notebook is empty"

        with open(path_to_book, "wb") as fh:
            pickle.dump(self.data, fh)
        return "Notebook saved"

    # deserialize Notebook
    def deserializer(self, path_to_book):
        keys_list = []
        try:
            with open(path_to_book, "rb") as fh:
                self.data = pickle.load(fh)
                keys_list = list(self.data)
                Notebook.index = max(keys_list)
                res = (
                    f"Saved notebook loaded, number of saved notes is {Notebook.index} "
                )
        except FileNotFoundError:
            res = "No file note_book.txt"

        return res
