import math

def calculate_parts(file_size, min_part_size=5 * 1024 * 1024, max_parts=10000):
    # Calculate the number of parts required based on file size and minimum part size
    num_parts = math.ceil(file_size / min_part_size)
    
    # Ensure we don't exceed the maximum parts allowed by S3 (10,000)
    if num_parts > max_parts:
        raise ValueError("File too large to be uploaded with 10,000 parts")
    
    return num_parts

