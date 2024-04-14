import boto3
import os
import json
import botocore
from flask import current_app as app

def publish_event(topic_arn, message):
    """
    Publishes a message to an SNS topic on AWS.

    Args:
        topic_arn (str): The Amazon Resource Name (ARN) of the SNS topic.
        message (dict): The message to be sent. It will be wrapped in the SNS JSON structure.

    Returns:
        dict: The response from the SNS publish operation.

    Raises:
        botocore.exceptions.ClientError: If there is an error while communicating with AWS SNS.
    """
    try:
        # Create an SNS client using credentials from the app's configuration
        sns_client = boto3.client(
            "sns",
            region_name=app.config.get("AWS_REGION", "us-east-1")
        )

        # Wrap message in the SNS JSON structure
        payload = {
            "default": json.dumps(message)
        }

        # Publish the message to the SNS topic
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(payload),
            MessageStructure='json'
        )

        return response

    except botocore.exceptions.ClientError as error:
        # Check if it's an 'InvalidClientTokenId' error, which typically happens due to invalid credentials
        if 'InvalidClientTokenId' in str(error):
            app.logger.error(f"Invalid AWS credentials: {error}")

        elif 'AccessDeniedException' in str(error):
            app.logger.error(f"Access Denied: Check AWS permissions: {error}")
            
        else:
            app.logger.error(f"Failed to publish SNS event: {error}")
        
        # Re-raise the error after logging it
        raise error

    except Exception as ex:
        # Catch any other unexpected exceptions
        app.logger.exception(f"Unexpected error occurred: {ex}")
        raise ex
