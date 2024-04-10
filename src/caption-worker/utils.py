import os 
from urllib.parse import urlparse, unquote


def create_presigned_url_from_s3_url(s3_url, s3_client, expiration=3600):
    parsed = urlparse(s3_url)
    bucket = parsed.netloc.split('.')[0]  # 'stress-app-video-bucket-example'
    key = unquote(parsed.path.lstrip('/'))  # decode %40 to @, etc.

    return s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expiration
    )


# Usage
#url = "https://stress-app-video-bucket-example.s3.us-east-1.amazonaws.com/shilu4577%40gmail.com/420623844-8ee879b8-3200-41bd-a015-674db3e13534.mp4"
#signed_url = create_presigned_url_from_s3_url(url)
#print(signed_url)
