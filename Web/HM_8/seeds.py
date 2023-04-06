import connect
import json

from models import Author, Quote

with open("data/authors.json", 'r') as file:
    data_authors = json.load(file)

with open("data/quotes.json", 'r') as file:
    data_quotes = json.load(file)

for d in data_authors:
    name = Author(fullname=d.get('fullname'))
    date = Author(born_date=d.get('born_date'))
    location = Author(born_location=d.get('born_location'))
    description = Author(description=d.get('description'))

for d in data_quotes:
    tags = d.get('tags')
    quote = d.get('quote')
    Quote(tags={"tags": tags}, author=Author(fullname=d.get('author')), quote=quote).save()
#     author=Author(fullname=d.get('author'))  author=d.get('author')
