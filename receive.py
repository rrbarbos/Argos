#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', '5672', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='teste')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue='teste', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
