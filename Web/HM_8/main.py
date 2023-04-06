from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://andrii_seeker:6dUwzpGQGxpl4YtH@cluster0.l8aoycl.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi('1')
)
db = client.book


if __name__ == '__main__':
    cats = db.cats.find()
    for i in cats:
        print(i.get('name'))