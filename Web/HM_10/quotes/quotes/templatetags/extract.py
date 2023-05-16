from bson import ObjectId
from django import template

from ..models import Author

register = template.Library()


def get_author(id_):
    obj = Author.objects.filter(id=ObjectId(id_))
    return obj['fullname'].text


register.filter('author', get_author)
