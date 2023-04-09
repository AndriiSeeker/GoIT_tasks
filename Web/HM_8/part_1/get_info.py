import redis
import time
from redis_lru import RedisLRU

from models import Quote, Author


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def mongo_db(command, value):
    try:
        out = set()
        match command:
            case 'name':
                quote_author = Author.objects(fullname__startswith=value)[0]
                for obj in Quote.objects(author=quote_author):
                    out.add(obj.quote)
            case 'tag':
                for quote in Quote.objects(tags__startswith=value):
                    out.add(quote.quote)
            case 'tags':
                value = value.split(",")
                for quote in Quote.objects(tags__in=value):
                    out.add(quote.quote)
        return out
    except IndexError:
        print("There is no such value in the table")


if __name__ == '__main__':
    print("Commands:\n   name:<value>\n   tag:<value>\n   tags:<value,value...>\n   exit")
    while True:
        user_input = str(input(">>>")).strip()
        if user_input == 'exit':
            print("Goodbye")
            break
        start = time.time()
        com, val = user_input.split(":")
        com = com.lower()
        quotes = mongo_db(com, val)
        print(*quotes, sep='\n')


