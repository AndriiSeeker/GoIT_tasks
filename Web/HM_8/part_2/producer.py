import faker
import pika
from random import choice

from models import Contacts

fake = faker.Faker('uk-UA')

num_of_people = 10


def add_to_queue(ids_sms, ids_email):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='task_mock', exchange_type='direct')

    channel.queue_declare(queue='Send_sms', durable=True)
    channel.queue_bind(exchange='task_mock', queue='Send_sms')

    channel.queue_declare(queue='Send_email', durable=True)
    channel.queue_bind(exchange='task_mock', queue='Send_email')

    for id in ids_sms:
        channel.basic_publish(
            exchange='task_mock',
            routing_key='Send_sms',
            body=id.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

        print(" [x] Sent by sms %r" % id)

    for id in ids_email:
        channel.basic_publish(
            exchange='task_mock',
            routing_key='Send_email',
            body=id.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

        print(" [x] Sent by email %r" % id)

    if ids_sms or ids_email:
        print(f"Sent {len(ids_sms + ids_email)} messages")
    else:
        print("Message has already been sent to each contact in db")
    connection.close()


def get_id_from_mongo():
    sms_id = []
    email_id = []
    contact_sms = Contacts.objects(boolean=False, method_sending='sms')
    contact_email = Contacts.objects(boolean=False, method_sending='email')
    for obj in contact_sms:
        sms_id.append(str(obj.id))
    for obj in contact_email:
        email_id.append(str(obj.id))
    return sms_id, email_id


def seeds():
    for _ in range(num_of_people):
        fullname = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        method_sending = choice(['sms', 'email'])
        Contacts(fullname=fullname, email=email, phone=phone, method_sending=method_sending).save()


if __name__ == '__main__':
    try:
        seeds() # add new contacts
        ids_sms, ids_email = get_id_from_mongo()
        add_to_queue(ids_sms, ids_email)
    except Exception as err:
        print(err)
