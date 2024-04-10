import boto3

_s3_client = None

def get_s3_client(access_key, secret_access_key, region_name):
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
            verify=True
        )
    return _s3_client
