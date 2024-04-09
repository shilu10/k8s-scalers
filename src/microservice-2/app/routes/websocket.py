from flask_socketio import emit, join_room, leave_room, socketio

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    emit('status_update', {'message': 'Connected to WebSocket for updates!'})
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('subscribe_job')
def handle_subscribe_job(data):
    job_id = data.get('job_id')
    
    if not job_id:
        emit('status_update', {'message': 'Job ID is required!'})
        return

    # Retrieve current job status from Redis
    status = redis_client.get(job_id)
    if status:
        emit('status_update', {'job_id': job_id, 'status': status.decode('utf-8')})
    else:
        emit('status_update', {'message': 'Job not found or invalid job_id'})

@socketio.on('job_progress')
def handle_job_progress(data):
    job_id = data.get('job_id')
    progress = data.get('progress')
    
    if job_id and progress:
        # Update Redis with job progress
        redis_client.set(job_id, f"{progress}%")
        emit('status_update', {'job_id': job_id, 'status': f"Progress: {progress}%"})
