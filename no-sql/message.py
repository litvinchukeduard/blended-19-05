from dataclasses import dataclass

import pika
import pika.connection
from db import User
import json

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
rabbit_mq_connection = pika.BlockingConnection(parameters)
rabbit_mq_channel = rabbit_mq_connection.channel()

def to_json(object):
    return json.dumps(object, default=lambda o: o.__dict__)

@dataclass
class Message:
    text: str
    sender: str
    recepient: str

def print_message(ch, method, properties, body):
    message_dict = json.loads(body)
    message_txt = f'{message_dict["sender"]}: {message_dict["text"]}'
    print(message_txt)

# A B C D E 
def send_rabbitmq_message(sender_username, message_text, recepient_username):
    sender = User.objects(username=sender_username)
    recepient = User.objects(username=recepient_username)
    if sender is None or recepient is None:
        print('Sender or recepient does not exist')
        return

    message = Message(text=message_text, sender=sender_username, recepient=recepient_username)
    rabbit_mq_channel.queue_declare(queue=recepient_username)
    rabbit_mq_channel.basic_publish(exchange='', routing_key=recepient_username, body=to_json(message))

def receive_rabbitmq_message(recepient_username):
    print('Recieving messages, use Ctrl C to exit')
    try:
        rabbit_mq_channel.basic_consume(queue=recepient_username, auto_ack=True, on_message_callback=print_message)
        rabbit_mq_channel.start_consuming()
    except KeyboardInterrupt:
        return

# if __name__ == '__main__':
#     send_message('test', 'Hello!', 'user')
#     receive_message('user')
