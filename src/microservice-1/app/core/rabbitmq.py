import pika 
from flask import current_app

_rabbit_mq_channel = None

def get_rabbitmq_channel():
    global _rabbit_mq_channel

    if not _rabbit_mq_channel:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=current_app.config['RABBITMQ_HOST']))
        _rabbit_mq_channel = connection.channel()
        _rabbit_mq_channel.queue_declare(queue=current_app.config["RABBITMQ_QUEUE_NAME"])

    return _rabbit_mq_channel

    
