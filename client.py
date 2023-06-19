import socket
import os
# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Command constants
COMMAND_LIST = 'LIST'
COMMAND_DOWNLOAD = 'DOWNLOAD'
COMMAND_UPLOAD = 'UPLOAD'

def send_command(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    if command == COMMAND_LIST:
        #LIST
        client_socket.sendall(command.encode())
        file_list = client_socket.recv(1024).decode()
        if file_list == 'EOF':
            print("Server side directory is empty")
            return
        print(file_list)

    if command.startswith(COMMAND_DOWNLOAD):
        #DOWNLOAD <filename>
        client_socket.sendall(command.encode())
        #check if file name is provided
        if len(command.split()) < 2:
            print("Please provide a file name")
            return
        filename = "downloaded_" + command.split()[1]
        file_sz = int(client_socket.recv(1024).decode())
        with open('client_side/'+filename, 'wb') as file:
            while file_sz > 0:
                data = client_socket.recv(1024)
                file.write(data)
                file_sz -= len(data)
        print(f"Finished downloading {filename}")

    if command.startswith(COMMAND_UPLOAD):
        #UPLOAD <filename> 
        if len(command.split()) < 2:
            print("Please provide a file name")
            return
        new_command = "UPLOAD" + " " + "uploaded_" + command.split()[1]
        #check if file exists or not in current directory
        if command.split()[1] not in os.listdir('.'):
            print(f"File not found: {command.split()[1]}")
            return
    
        client_socket.sendall(new_command.encode())
        file_sz = os.path.getsize(command.split()[1])
        print("File size: ", file_sz, "bytes")
        client_socket.sendall(str(file_sz).encode())
        print("Uploading file to server")
        filename = command.split()[1]
        try:
            with open(filename, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
            print(f"Finished uploading {filename}")
        except FileNotFoundError:
            print(f"File not found: {filename}") 

    client_socket.close()

# Client interaction loop
while True:
    # make below print more readable
    user_input = input("Enter a command \nLIST : List all the directories in server side, \nDOWNLOAD <filename> : Download the file from server, \nUPLOAD <filename> : Upload the file to server \n")
    if user_input == 'QUIT':
        break

    send_command(user_input)
