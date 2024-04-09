import json
import os 
import boto3


def handler(event, context):
    """
    Main Lambda handler function
    Parameters:
        event: Dict containing the Lambda function event data
        context: Lambda runtime context
    Returns:
        Dict containing status message
    """
    try:
        s3_client = boto3.client("s3")
        user_email = event.get("email")
        bucket_name = os.environ["BUCKET_NAME"]
        folder_name = user_email

        s3_client.put_object(Bucket=bucket_name, Key=folder_name)

        return {"success": True}

    except Exception as err:
        raise 
