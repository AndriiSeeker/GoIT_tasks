from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, ModelChoiceField, Select, \
    SelectMultiple
from .models import Quote, Author, Tag


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, required=True, widget=TextInput())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all().order_by("name"), required=True,
                                    widget=SelectMultiple())
    author = ModelChoiceField(queryset=Author.objects.all().order_by("fullname"), widget=Select())

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, widget=TextInput())
    born_date = CharField(max_length=50, widget=TextInput())
    born_location = CharField(max_length=150, widget=TextInput())
    description = CharField(widget=TextInput())

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class TagForm(ModelForm):
    name = CharField(max_length=50, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]