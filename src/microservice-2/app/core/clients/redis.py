import redis 
from flask import current_app 

_redis_client = None

def get_redis_client(host, port, db):
    global _redis_client
    
    if not _redis_client:
        _redis_client = redis.Redis(host = host, 
                        port = port,
                        db = db
                    )
        
    return _redis_client