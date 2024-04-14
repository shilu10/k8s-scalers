import boto3

_s3_client = None

def get_s3_client(region_name):
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            region_name=region_name,
            verify=True
        )
        
    return _s3_client
