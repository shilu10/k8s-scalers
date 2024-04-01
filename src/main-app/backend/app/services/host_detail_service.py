import socket


def get_host_details():
    hostname = socket.gethostname()

    try:
        ip = socket.gethostbyname(hostname)

    except socket.gaierror:
        ip = 'Unavailable'

    return {
        "Hostname": hostname,
        "IP": ip
    }
