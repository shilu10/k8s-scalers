import pika
import json

_rabbitmq_client = None  # global instance for reuse

class RabbitMQClient:
    def __init__(self, host="rabbitmq", queue_name="stress"):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name, durable=False)

    def publish_message(self, message: dict):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=1  # non-persistent
            )
        )

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

def init_rabbitmq_connection(host="rabbitmq", queue_name="stress"):
    global _rabbitmq_client
    _rabbitmq_client = RabbitMQClient(host, queue_name)

def get_rabbitmq_client():
    return _rabbitmq_client

def close_rabbitmq_connection():
    if _rabbitmq_client:
        _rabbitmq_client.close()
