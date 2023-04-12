import json

from models import Authors, Quotes


def write_to_db():
    with open("authors.json", 'r', encoding='utf-8') as file:
        data_authors = json.load(file)

    with open("quotes.json", 'r', encoding='utf-8') as file:
        data_quotes = json.load(file)

    for d in data_authors:
        name = d.get('fullname')
        date = d.get('born_date')
        location = d.get('born_location')
        description = d.get('description')
        Authors(fullname=name, born_date=date, born_location=location, description=description).save()

    for d in data_quotes:
        tags = d.get('tags')
        quote = d.get('quote')
        author = Authors.objects(fullname=d.get('author'))
        Quotes(tags=tags, quote=quote, author=author[0]).save()
