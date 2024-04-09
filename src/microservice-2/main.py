from app import create_app

# Create app and socketio instances
#app, socketio = create_app()

app = create_app()
if __name__ == "__main__":
    # Run with SocketIO support
    #socketio.run(app, debug=True, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5000)
