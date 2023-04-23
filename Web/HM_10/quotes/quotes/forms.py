import os
import sys

from django.forms import ModelForm, CharField, TextInput
from django.contrib.postgres.forms import SimpleArrayField

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models import Quote


class NoteForm(ModelForm):
    quote = CharField(min_length=5, required=True, widget=TextInput())
    author = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    tags = SimpleArrayField(min_length=10, max_length=150, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
