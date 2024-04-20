import boto3
from urllib.parse import urlparse, unquote
from logger import setup_rotating_logger
import os 

_logger = setup_rotating_logger()

def create_presigned_url_from_s3_url(s3_url: str, s3_client, expiration=3600):
    try:
        parsed_url = urlparse(s3_url)
        bucket = parsed_url.netloc.split('.')[0]
        key = unquote(parsed_url.path.lstrip('/'))

        _logger.info(f"Bucket: {bucket}")
        _logger.info(f"Key: {key}")

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration,
        )

        return presigned_url
    
    except Exception as err:
        _logger.error(err)
        os.exit()


def url_encode(text):
    from urllib.parse import quote
    return quote(text, safe='')