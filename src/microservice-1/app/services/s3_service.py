import boto3 
from flask import current_app
from ..core.s3 import get_s3_client


def upload_to_bucket(filename, video_file):
    try:
        s3_client = get_s3_client()

        response = s3_client.put_object(
                Body = video_file,
                Bucket = current_app.config["OBJECT_STORE_BUCKET_NAME"], # 'k8s-scalers-example-bucket'
                Key = filename,
            )
        
        return {
            "success": True,
        }
        
    except Exception as err:
        return {
            "success": False,
            "reason": str(err)
        }
    
