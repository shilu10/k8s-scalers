import boto3, os
from botocore.exceptions import ClientError
from flask import current_app as app, jsonify
from ..core.s3 import get_s3_client
from ..core.errors import ClientErrorException, ValueErrorException
from ..core.utils import calculate_parts


def initiate_multipart_upload(s3_client, bucket_name, object_path):
    """Initiate a multipart upload to get the UploadId"""
    app.logger.info("Initiating multipart upload for: %s", object_path)
    response = s3_client.create_multipart_upload(
        Bucket=bucket_name,
        Key=object_path
    )
    app.logger.debug("UploadId received: %s", response['UploadId'])
    return response['UploadId']


def generate_presigned_urls(s3_client, bucket_name, object_path, upload_id, part_count):
    """Generate pre-signed URLs for each part of the file"""
    urls = []
    for part_number in range(1, part_count + 1):
        url = s3_client.generate_presigned_url(
            ClientMethod='upload_part',
            Params={
                'Bucket': bucket_name,
                'Key': object_path,
                'UploadId': upload_id,
                'PartNumber': part_number,
            },
            ExpiresIn=app.config.get("PRESIGNED_URL_EXPIRATION")
        )
        urls.append({'partNumber': part_number, 'url': url})
        app.logger.debug("Generated URL for part %s", part_number)
    return urls


def generate(file_name, email, file_size):
    """Main function to generate multipart upload pre-signed URLs"""
    object_path = os.path.join(email, file_name)
    app.logger.info("Object Path Creation Started: %s", object_path)
    bucket_name = app.config.get("OBJECT_STORE_BUCKET_NAME")

    s3_client = get_s3_client()
    app.logger.info("Initialized S3 Client")

    try:
        # Step 1: Initiate the multipart upload and get UploadId
        upload_id = initiate_multipart_upload(s3_client, bucket_name, object_path)

        # Step 2: Generate pre-signed URLs for each part
        part_counts = calculate_parts(file_size=file_size)
        app.logger.info("Number of parts calculated: %s", part_counts)
        presigned_urls = generate_presigned_urls(s3_client, bucket_name, object_path, upload_id, part_count=part_counts)

        app.logger.info("PreSigned URLs Generated for: %s", email)
        return {
            "uploadId": upload_id,
            "parts": presigned_urls,
            "fileUrl": f"https://{bucket_name}.s3.amazonaws.com/{object_path}"
        }

    except ClientError as e:
        app.logger.warning("AWS ClientError: %s", e)
        raise ClientErrorException(e)

    except ValueError as e:
        app.logger.warning("Invalid file size or input: %s", e)
        raise ValueErrorException(e)
