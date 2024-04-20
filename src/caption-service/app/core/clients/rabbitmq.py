import ssl
import json
import logging
import pika

logging.basicConfig(level=logging.INFO)

_rabbitmq_client = None  # Global instance for reuse

class RabbitMQClient:
    def __init__(self, broker_id, region, username, password, queue_name="stress", virtual_host="/", endpoint_suffix=None):
        self.broker_id = broker_id
        self.region = region
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.virtual_host = virtual_host
        self.endpoint_suffix = endpoint_suffix or f"mq.{region}.on.aws"
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        """Establish RabbitMQ connection and channel with SSL."""
        try:
            logging.info(f"{self.username}, {self.password}")
            url = f"amqps://{self.username}:{self._url_encode(self.password)}@{self.broker_id}.{self.endpoint_suffix}:5671/"
            parameters = pika.URLParameters(url)
            ssl_context = ssl.create_default_context()
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            logging.info("RabbitMQ connection established.")

        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def _url_encode(self, text):
        from urllib.parse import quote
        return quote(text, safe='')

    def publish_message(self, message: dict):
        """Publish a message, reconnecting if needed."""
        if not self.channel or self.channel.is_closed:
            self._connect()

        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # Persistent
            )
            logging.info("Message published.")
            
        except Exception as e:
            logging.warning(f"Publish failed: {e}. Reconnecting and retrying...")
            self._connect()
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )

    def close(self):
        """Close the channel and connection."""
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and self.connection.is_open:
            self.connection.close()
        logging.info("RabbitMQ connection closed.")

def init_rabbitmq_connection(broker_id, region, username, password, queue_name="stress", virtual_host="/", endpoint_suffix=None):
    global _rabbitmq_client
    if _rabbitmq_client is None:
        _rabbitmq_client = RabbitMQClient(
            broker_id, region, username, password, queue_name, virtual_host, endpoint_suffix
        )
    return _rabbitmq_client

def get_rabbitmq_client():
    if not _rabbitmq_client:
        raise Exception("RabbitMQ client not initialized. Call init_rabbitmq_connection() first.")
    
    return _rabbitmq_client

def close_rabbitmq_connection():
    global _rabbitmq_client
    if _rabbitmq_client:
        _rabbitmq_client.close()
        _rabbitmq_client = None

if __name__ == "__main__":
    try:
        client = init_rabbitmq_connection(
            broker_id="xxxxxxxxxxxx",
            region="us-east-1",
            username="xxx",
            password="xxxxxx",
            queue_name="stress",
            virtual_host="/",
            endpoint_suffix="mq.us-east-1.on.aws"
        )
        client.publish_message({"status": "connected", "message": "Hello RabbitMQ from Python!"})
        print("✅ Message sent successfully.")

    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        traceback.print_exc()
        
    finally:
        close_rabbitmq_connection()