import pika 
import json, os
from flask import current_app 
from ..core.rabbitmq import get_rabbitmq_channel


def publish_message(job_id, filename):
    try:
        rabbitmq_channel = get_rabbitmq_channel()

        rabbitmq_body = dict()
        rabbitmq_body["job_id"] = job_id
        rabbitmq_body["filename"] = filename

        rabbitmq_channel.basic_publish(exchange='', 
                              routing_key=os.environ["RABBITMQ_QUEUE_NAME"], 
                              body=json.dumps(rabbitmq_body)
                            )
        
        return {
            "success": True,
        }

    except Exception as err:
          return {
            "success": False,
            "reason": str(err)
        }