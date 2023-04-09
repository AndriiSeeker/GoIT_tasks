import time
from bson import ObjectId

import pika

from models import Contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='Send_sms', durable=True)
print('[*] Waiting for sms. To exit press CTRL+C')


def change_val_in_db(id):
    contact = Contacts.objects(id=ObjectId(id))[0]
    contact.update(boolean=True)


def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received {message}")
    time.sleep(1)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    change_val_in_db(message)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='Send_sms', on_message_callback=callback)


if __name__ == '__main__':
    list_of_ids = []
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()
    print(list_of_ids)
