import pika
from redis_client import get_redis_client
from config import Config
import json
import asyncio
from deepgram_transcript import stream_from_s3
from logger import setup_rotating_logger
import threading
from s3_client import get_s3_client
from utils import create_presigned_url_from_s3_url, url_encode
import ssl

# Initialize
config = Config()
_logger = setup_rotating_logger()
redis_client = get_redis_client(
    config.REDIS_HOST,
    config.REDIS_PORT,
    config.REDIS_DB,
    use_ssl=False  # Set True if you're using TLS (rediss)
)
# Setup RabbitMQ SSL connection
url = f"amqps://{config.MQ_USERNAME}:{url_encode(config.MQ_PASSWORD)}@{config.MQ_BROKER_ID}.{config.MQ_ENDPOINT_SUFFIX}:5671/"
parameters = pika.URLParameters(url)
ssl_context = ssl.create_default_context()
parameters.ssl_options = pika.SSLOptions(context=ssl_context)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=config.MQ_QUEUE_NAME, durable=True)


def run_job(video_url, presigned_video_url, job_id):
    """Run the Deepgram job asynchronously, handling Redis and logging."""
    try:
        asyncio.run(stream_from_s3(
            video_url,
            presigned_video_url,
            deepgram_api_key=config.DEEPGRAM_API_KEY,
            deepgram_ws_url=config.DEEPGRAM_WS_URL,
            job_id=job_id,
            redis_client=redis_client
        ))
        redis_client.set(job_id, "Processed")
        redis_client.publish("my_channel", json.dumps({"job_id": job_id, "status": "Processed"}))
        _logger.info("✅ Completed processing for job_id: %s", job_id)

    except Exception as e:
        redis_client.set(job_id, "failed")
        redis_client.publish("my_channel", json.dumps({"job_id": job_id, "status": "failed"}))
        _logger.exception(f"❌ Job {job_id} failed due to: {e}")


def process_job(ch, method, properties, body):
    """Callback for consuming a job from the queue."""
    try:
        job = json.loads(body)
        job_id = job.get('job_id')
        video_url = job.get('video_url')
        _logger.info(f"📥 Received job_id: {job_id}")

        s3_client = get_s3_client(config.AWS_REGION)
        presigned_video_url = create_presigned_url_from_s3_url(video_url, s3_client)
        _logger.info(f"🔐 Presigned S3 URL generated for job_id: {job_id}")

        _logger.info("🔌 Redis client ping: %s", redis_client.ping())


        _logger.info("📡 About to set Redis status for job_id: %s", job_id)
        redis_client.set(job_id, "processing")
        _logger.info("✅ Redis SET done")

        redis_client.publish("my_channel", json.dumps({"job_id": job_id, "status": "processing"}))
        _logger.info("✅ Redis PUBLISH done")


        # Run job in background thread
        thread = threading.Thread(
            target=lambda: run_job_and_ack(ch, method, video_url, presigned_video_url, job_id),
            daemon=True
        )
        thread.start()

    except Exception as e:
        _logger.exception(f"❌ Exception occurred while handling job: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def run_job_and_ack(ch, method, video_url, presigned_video_url, job_id):
    """Helper to run job and send RabbitMQ ack/nack safely."""
    try:
        run_job(video_url, presigned_video_url, job_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        _logger.info("✅ Acked job: %s", job_id)
    except Exception as e:
        _logger.exception(f"❌ Exception in threaded job: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


# Configure queue consumer
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.MQ_QUEUE_NAME, on_message_callback=process_job)

_logger.info("📡 Worker is waiting for tasks...")
channel.start_consuming()
