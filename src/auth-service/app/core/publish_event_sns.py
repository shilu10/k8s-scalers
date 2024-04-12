import boto3, os, json
import botocore
from flask import current_app as app


def publish_event(topic_arn, message):
    try:
        sns_client = boto3.client(
            "sns",
            aws_access_key_id=app.config["AWS_ACCESS_KEY"],
            aws_secret_access_key=app.config["AWS_SECRET_KEY"],
            region_name=app.config.get("AWS_REGION", "us-east-1")
        )

        # Wrap message in the SNS JSON structure
        payload = {
            "default": json.dumps(message)
        }

        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(payload),
            MessageStructure='json'
        )

        return response

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'LimitExceededException':
            app.logger.warning('API call limit exceeded; backing off and retrying...')
        else:
            app.logger.error(f"Failed to publish SNS event: {error}")
            raise error
