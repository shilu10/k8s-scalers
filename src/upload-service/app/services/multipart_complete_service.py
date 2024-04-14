from flask import current_app as app


def complete_multipart_upload(s3_client, bucket_name, object_path, upload_id, parts):
    """
    Completes a multipart upload in S3 by assembling previously uploaded parts.

    This method finalizes the upload process by instructing S3 to combine the uploaded
    parts into a single object. All parts must be uploaded before this function is called.

    Args:
        s3_client (boto3.client): The initialized Boto3 S3 client.
        bucket_name (str): The name of the S3 bucket where the object is stored.
        object_path (str): The key (path) for the object in the bucket.
        upload_id (str): The UploadId associated with the multipart upload session.
        parts (list of dict): A list of parts, each with:
            - 'ETag' (str): The ETag returned from S3 for the uploaded part.
            - 'PartNumber' (int): The part number.

    Returns:
        dict: The response from the S3 `complete_multipart_upload` API call, typically
              including the object's ETag and location.

    Raises:
        botocore.exceptions.ClientError: If the complete call fails due to an S3 error.
    """
    app.logger.info("Completing multipart upload for: %s", object_path)
    return s3_client.complete_multipart_upload(
        Bucket=bucket_name,
        Key=object_path,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
