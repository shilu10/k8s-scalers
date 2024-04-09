import boto3, os
from botocore.exceptions import ValidationException
from errors import ValidationErrrorException


def publish_event(topic_arn, message):
    try:
        sns_client = boto3.client("sns", 
                                aws_access_key_id=os.environ["AWS_ACCESS_KEY"], 
                                aws_secret_access_key=os.environ["AWS_SECRET_KEY"])

        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageStructure='json'
        )

        return response
    
    except ValidationException as err:
        raise ValidationErrrorException("Error During Validation: %s", err)
