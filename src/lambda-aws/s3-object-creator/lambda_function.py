import json
import os
import boto3


def handler(event, context):
    """
    Lambda function to process SNS events and create a folder in S3.
    """
    try:
        s3_client = boto3.client("s3")
        bucket_name = os.environ["BUCKET_NAME"]

        for record in event.get("Records", []):
            sns_message = record["Sns"]["Message"]
            message_dict = json.loads(sns_message)

            user_email = message_dict.get("email")

            if not user_email:
                continue  # or log an error

            folder_name = f"{user_email}/"  # add trailing slash to create a folder-like object

            # Put an empty object to represent the folder
            s3_client.put_object(Bucket=bucket_name, Key=folder_name)

        return {"success": True}

    except Exception as err:
        print(f"Error processing event: {err}")
        raise
