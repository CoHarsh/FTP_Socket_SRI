import socket
import os
import time
# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Command constants
COMMAND_LIST = 'LIST'
COMMAND_DOWNLOAD = 'DOWNLOAD'
COMMAND_UPLOAD = 'UPLOAD'

# Data constants
CHUNK_SIZE = 1024

def handle_command(connection, address):
    while True:
        command = connection.recv(1024).decode().strip()

        if command == COMMAND_LIST:
            #list all the files in server_side directory
            # in microseconds
            start_time = time.time()
            print(f"Received command: {command}")
            #If empty directory, send empty string
            if not os.listdir('server_side'):
                connection.sendall('EOF'.encode())
                print("Server side directory is empty")
                continue
            file_list = os.listdir('server_side')
            file_list = '\n'.join(file_list)
            connection.sendall(file_list.encode())
            end_time = time.time()
            print(f"Time taken to list files: {(end_time - start_time) * 1000000} us")
            continue
        elif command.startswith(COMMAND_DOWNLOAD):
            start_time = time.time()
            print(f"Received command: {command}")
            filename = command.split()[1]
            #check if file exists in server_side directory
            if filename not in os.listdir('server_side'):
                connection.sendall(b'File not found')
                continue
            print(f"Sending {filename} to {address[0]}:{address[1]}")
            try:
                with open('server_side/' + filename, 'rb') as file:
                    while True:
                        data = file.read(CHUNK_SIZE)
                        if not data:
                            break
                        connection.sendall(data)
                print(f"Finished sending {filename}")
                connection.sendall(b'EOF')
                end_time = time.time()
                print(f"Time taken to download file: {(end_time - start_time) * 1000000} us")
            except FileNotFoundError:
                connection.sendall(b'File not found')
            continue
        elif command.startswith(COMMAND_UPLOAD):
            start_time = time.time()
            print(f"Received command: {command}")
            filename = command.split()[1]
            print(f"Receiving {filename} from {address[0]}:{address[1]}")
            try:
                with open('server_side/' + filename, 'wb') as file:
                    while True:
                        data = connection.recv(CHUNK_SIZE)
                        if data == b'EOF':
                            break
                        file.write(data)
                print(f"Finished receiving {filename}")
                end_time = time.time()
                print(f"Time taken to upload file: {(end_time - start_time) * 1000000} us")
            except FileNotFoundError:
                connection.sendall(b'File not found')
            continue
        else:
            print(f"Invalid command: {command}")
            break

    connection.close()

# Start the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address[0]}:{client_address[1]}")

    handle_command(client_socket, client_address)
