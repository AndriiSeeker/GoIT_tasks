import json

from models import Author, Quote


with open("data/authors.json", 'r', encoding='utf-8') as file:
    data_authors = json.load(file)

with open("data/quotes.json", 'r', encoding='utf-8') as file:
    data_quotes = json.load(file)

for d in data_authors:
    name = d.get('fullname')
    date = d.get('born_date')
    location = d.get('born_location')
    description = d.get('description')
    Author(fullname=name, born_date=date, born_location=location, description=description).save()

for d in data_quotes:
    tags = d.get('tags')
    quote = d.get('quote')
    author = Author.objects(fullname=d.get('author'))
    Quote(tags=tags, quote=quote, author=author[0]).save()
