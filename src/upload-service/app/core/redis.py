import redis 
from flask import current_app 

_redis_client = None

def get_redis_client():
    global _redis_client
    
    if not _redis_client:
        _redis_client = redis.Redis(host = current_app.config["REDIS_HOST"], 
                        port = current_app.config["REDIS_PORT"]
                    )
        
    return _redis_client