from flask import current_app as app 


def complete_multipart_upload(s3_client, bucket_name, object_path, upload_id, parts):
    """Complete the multipart upload by combining all parts"""
    app.logger.info("Completing multipart upload for: %s", object_path)
    return s3_client.complete_multipart_upload(
        Bucket=bucket_name,
        Key=object_path,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )