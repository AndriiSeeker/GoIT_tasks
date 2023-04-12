from mongoengine import *


connect(host="mongodb+srv://andrii_seeker:6dUwzpGQGxpl4YtH@cluster0.l8aoycl.mongodb.net/?retryWrites=true&w=majority")


class Authors(Document):
    fullname = StringField(max_length=250)
    born_date = StringField(max_length=250)
    born_location = StringField(max_length=250)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=100))
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField(required=True)
    meta = {'allow_inheritance': True}

