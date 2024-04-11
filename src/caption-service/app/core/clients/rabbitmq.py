import pika
import json

_rabbitmq_client = None  # global instance for reuse

class RabbitMQClient:
    def __init__(self, host="rabbitmq", queue_name="stress"):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        """Re-establish the RabbitMQ connection and channel."""
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=False)
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            raise

    def publish_message(self, message: dict):
        """Publish a message to RabbitMQ, reconnecting if necessary."""
        if not self.channel or self.channel.is_closed:
            self._connect()  # Reconnect if channel is closed or None
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=1)  # non-persistent
            )
        except Exception as e:
            print(f"Failed to publish message: {e}")
            self._connect()  # Try reconnecting if publish fails

    def close(self):
        """Close the connection and channel."""
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and self.connection.is_open:
            self.connection.close()


def init_rabbitmq_connection(host="rabbitmq", queue_name="stress"):
    global _rabbitmq_client
    _rabbitmq_client = RabbitMQClient(host, queue_name)

def get_rabbitmq_client():
    return _rabbitmq_client

def close_rabbitmq_connection():
    if _rabbitmq_client:
        _rabbitmq_client.close()
