import pika
import json

# RabbitMQ connection parameters
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='stress')

# Sample JSON message
message = {
    'job_id': '1234511111',
    'video_url': 'https://stress-app-video-bucket-example.s3.us-east-1.amazonaws.com/362781088-f6de3ae5-bcc9-480c-bc46-dee69ec22795_1.mp4?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCiTj8al3DNNhwI1CX22uwc8%2Bdvq4TI%2Bp42PhBwa%2Be0lQIgMN4sxPvVkde5%2Fu4DYaJziq2QGoSwaj5Cl9oGvBQ96QAquQMIPBAAGgw1MzMyNjc0NTM3NTEiDEAQ2ls%2BX85WSOrO1yqWA7hf4OhjdVFLUz22AZ4INBXHYrh3sORVN2PkGWD3WTAKleNdmXxoc6XHO%2BnVEIOIr%2BpKSeMuNrUhy22xtpxfsKgb%2F9UUdEZKTZFLfvEOIBsRiTCylLrf9gRw9ojaLpNLu6QHDtDEiO31ppGbYy%2FBGRpBARWpYwHqXHOhmCQnrbWpJe7WVRyaimBzY1XHoJASJc5mS9S7u4iROurgj2PCakMhFRm1VZ6MXKC4lteNJTJwbx2TgfRzmG%2FkmLGXPAlo5EU9iQCGOyLzx39NA66itLLD3cxgTNCFyOInQMdjBr6hspb6U5Pp1RMDxYH%2FFFyidrf9y%2FN6sIPmEAZ0H2b0wZ056mnITcCebKPaK4QJ%2F4FbO9%2BoodBL%2F0JYd9N%2BVoVdL0i5I4ZFsWV8KUg2l4IpxBmrc4W0fjB%2BxsyRrSnyGgQb73WxCCZ%2FM9CJ6KfVUL4tBjuc5rBMddqSn5d8K%2F%2B%2BL72mBlGrm%2FvuxJqPVU%2FCA%2FiwlpzlXokcoJ67Vl8wLqduBHHs0R5IzM5WVwAN2PgrH0WYhPc22UowncXlwAY63gJlT8GLOUb0s9%2F2xEjQiohthPKFzRDDbteSyvvmoJIlE3IKuIT1tR7XNIJV8PZCMIi3ETqj%2FdeYhJJ7kcXD6pMEmrUb0iJRvQ7tRq4xepR0z4WELKpN8LJHRCXQy9QBJHT%2BlK2cRjSa5IMX5wlJpQVvFbWuzogXkWa95L7Ko0TNs58VEiIQ8opbuCbX4VmWu%2F8KPKM8t0POeddKTtQVkSPQRf5k27mdl%2Fm0Eg23AAGSmk45ezp%2B5AXBd6YUPOCVvfOvrGxAQ79Mlhtyf6%2BQDoYFtadChDW9B%2Bdf74KAEtTw1sAcoxm2AzP6sr16MXIyKYww6fJYtXo8NslqJ7Y9Gss5pUnbIriaqCd1Wnp8uAVixNY5ytXjZAHrRPfkX%2BzZoF3blNwabIAD9NqKuHY%2BJGAo0r3oTnJP%2FxLRR%2BqUbMEBf337je3d07TkAodu7RgSNSe07ohPYAeh2DhDXEVp8g%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAXYKJXS43TLFGATDE%2F20250506%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250506T025700Z&X-Amz-Expires=7200&X-Amz-SignedHeaders=host&X-Amz-Signature=3f651c969a1093d0ce4eb49a993b8479044707d83661ddc08b9fb3b4c597dcce',
    'language': 's',
    'user': 'shilu'
}

# Convert dict to JSON string
json_message = json.dumps(message)

# Publish to the queue
channel.basic_publish(
    exchange='',
    routing_key='stress',
    body=json_message
)

print(" [x] Sent JSON message to 'json_queue'")

# Close connection
connection.close()
