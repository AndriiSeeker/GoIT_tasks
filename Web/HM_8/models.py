from mongoengine import EmbeddedDocument, Document, ReferenceField
from mongoengine.fields import ListField, StringField, DictField


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = DictField(ListField(StringField()))
    author = ReferenceField(Author)
    quote = StringField()
    meta = {'allow_inheritance': True}

