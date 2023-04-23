import os
import sys

from bson import ObjectId
from django import template

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import get_mongo

register = template.Library()


def get_author(id_):
    db = get_mongo()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    return author['fullname']


register.filter('author', get_author)

if __name__ == '__main__':
    pass
