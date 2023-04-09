from mongoengine import *


connect(host="mongodb+srv://andrii_seeker:6dUwzpGQGxpl4YtH@cluster0.l8aoycl.mongodb.net/?retryWrites=true&w=majority")


class Contacts(Document):
    fullname = StringField(max_length=250)
    email = StringField(max_length=250)
    phone = StringField(max_length=250)
    method_sending = StringField(max_length=250, default="sms")
    boolean = BooleanField(default=False)
