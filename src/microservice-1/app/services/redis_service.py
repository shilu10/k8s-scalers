import redis 
from flask import current_app 
from ..core.redis import get_redis_client


def put_object(job_id):
    try:
        redis_client = get_redis_client()
        # job status
        status_dict = dict()
        status_dict["job_id"] = job_id
        status_dict["status"] = "Processing"
        status_dict["progress"] = 0

        redis_client.hset(job_id, mapping=status_dict)

        return {
            "success": True,
        }

    except Exception as err:
        return {
            "success": False,
            "reason": str(err)
        }