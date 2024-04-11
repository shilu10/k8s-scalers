import pika
from redis_client import get_redis_client
from config import Config
import json
import asyncio
from deepgram_transcript import stream_from_s3
from logger import setup_rotating_logger
import threading
from s3_client import get_s3_client
from utils import create_presigned_url_from_s3_url


# initialize config
config = Config()

# initialize logger
_logger = setup_rotating_logger()

# Initialize Redis for tracking job status
redis_client = get_redis_client(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=config.RABBITMQ_HOST,
        heartbeat=600,
        blocked_connection_timeout=300
    )
)
channel = connection.channel()

# Declare the queue for receiving tasks
channel.queue_declare(queue=config.RABBITMQ_QUEUE_NAME, durable=False)


def run_job_in_thread(video_url, presigned_video_url, job_id):
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
        redis_pub_sub_message = {"job_id": job_id, "status": "Processed"}
        redis_client.publish("my_channel", json.dumps(redis_pub_sub_message))
        _logger.info("Completed processing for %s", job_id)

    except Exception as e:
        redis_client.set(job_id, "failed")
        redis_client.publish("my_channel", "failed")
        _logger.exception(f"Job {job_id} failed due to: {e}")


def process_job(ch, method, properties, body):
    job = json.loads(body)
    job_id = job.get('job_id')
    video_url = job.get('video_url')

    s3_client = get_s3_client(config.AWS_ACCESS_KEY, config.AWS_SECRET_ACCESS_KEY, config.AWS_REGION)
    presigned_video_url = create_presigned_url_from_s3_url(video_url, s3_client)

    redis_client.set(job_id, "processing")
    redis_client.publish("my_channel", "processing")
    _logger.info("Started processing for %s", job_id)

    # Start async job in a separate thread
    thread = threading.Thread(target=run_job_in_thread, args=(video_url, presigned_video_url, job_id))
    thread.start()

    # Acknowledge the message *immediately* after dispatching
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Start consuming messages
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.RABBITMQ_QUEUE_NAME, on_message_callback=process_job)

_logger.info("Worker is waiting for tasks...")
channel.start_consuming()
