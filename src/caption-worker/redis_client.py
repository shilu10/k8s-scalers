from redis import Redis
import logging

_logger = logging.getLogger(__name__)

_redis_client = None

def get_redis_client(host, port, db, use_ssl=False):
    global _redis_client

    if not _redis_client:
        try:
            _redis_client = Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,  # handles str/json
                ssl=use_ssl,
                socket_connect_timeout=5  # avoid long hangs
            )
            _redis_client.ping()
            _logger.info("✅ Redis client successfully connected!")
            
        except Exception as e:
            _logger.exception("❌ Redis connection failed: %s", e)
            raise

    return _redis_client
