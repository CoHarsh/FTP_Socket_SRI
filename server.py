import socket
import os
import time

# Server configuration
SERVER_HOST = '127.0.0.1'
COMMAND_PORT = 12345
DATA_PORT = 12346  # Port for data channel

# Command constants
COMMAND_LIST = 'LIST'
COMMAND_DOWNLOAD = 'DOWNLOAD'
COMMAND_UPLOAD = 'UPLOAD'

# time_plot data
LIST_TIME='list_timedata.csv'
DOWNLOAD_TIME='download_timedata.csv'
UPLOAD_TIME='upload_timedata.csv'

# Data constants
CHUNK_SIZE = 1024

def handle_command(command_socket, address):
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind((SERVER_HOST, DATA_PORT))
    data_socket.listen(1)

    while True:
        command = command_socket.recv(1024).decode().strip()

        if command == COMMAND_LIST:
            # List all the files in the server_side directory
            # in microseconds
            start_time = time.time()
            print(f"Received command: {command}")
            # If empty directory, send empty string
            if not os.listdir('server_side'):
                command_socket.sendall('EOF'.encode())
                print("Server-side directory is empty")
                continue
            file_list = os.listdir('server_side')
            file_list = '\n'.join(file_list)
            command_socket.sendall(file_list.encode())
            end_time = time.time()
            print(f"Time taken to list files: {(end_time - start_time) * 1000000} us")
            # Log the time to a CSV file
            with open('plot_data/list_timedata.csv', 'a') as file:
                file.write(f"{len(file_list)}, {(end_time - start_time) * 1000000}\n")
            continue

        elif command.startswith(COMMAND_DOWNLOAD):
            start_time = time.time()

            print(f"Received command: {command}")
            filename = command.split()[1]
            # Check if file exists in server_side directory
            if filename not in os.listdir('server_side'):
                command_socket.sendall(b'File not found')
                continue
            print(f"Sending {filename} to {address[0]}:{address[1]}")

            data_connection, _ = data_socket.accept()
            file_size = os.path.getsize('server_side/' + filename)
            data_connection.sendall(str(file_size).encode())
            try:
                with open('server_side/' + filename, 'rb') as file:
                    while True:
                        data = file.read(CHUNK_SIZE)
                        if not data:
                            break
                        data_connection.sendall(data)
                print(f"Finished sending {filename}")
                end_time = time.time()
                file_size = os.path.getsize('server_side/' + filename)
                print(f"Time taken to download file: {(end_time - start_time) * 1000000} us")
                # Log the time to a CSV file (in download_timedata.csv)
                with open('plot_data/download_timedata.csv', 'a') as file:
                    file.write(f"{file_size}, {(end_time - start_time) * 1000000}\n")

            except FileNotFoundError:
                command_socket.sendall(b'File not found')
            continue

        elif command.startswith(COMMAND_UPLOAD):
            start_time = time.time()
            file_size = command_socket.recv(1024).decode().strip()
            file_size = int(file_size)
            print(f"Received command: {command}")
            filename = command.split()[1]
            print(f"Receiving {filename} from {address[0]}:{address[1]}")

            data_connection, _ = data_socket.accept()
            try:
                with open('server_side/' + filename, 'wb') as file:
                    while int(file_size) > 0:
                        data = data_connection.recv(CHUNK_SIZE)
                        if not data:
                            break
                        file.write(data)
                        file_size -= len(data)
                print(f"Finished receiving {filename}")
                end_time = time.time()
                print(f"Time taken to upload file: {(end_time - start_time) * 1000000} us")
                file_sz = os.path.getsize('server_side/' + filename)
                # Log the time to a CSV file
                with open('plot_data/upload_timedata.csv', 'a') as file:
                    file.write(f"{file_sz}, {(end_time - start_time) * 1000000}\n")

            except FileNotFoundError:
                command_socket.sendall(b'File not found')
            continue

        else:
            break

    command_socket.close()
    data_socket.close()

# Start the server
command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.bind((SERVER_HOST, COMMAND_PORT))
command_socket.listen(1)

print(f"Server listening on {SERVER_HOST}:{COMMAND_PORT}")

while True:
    client_socket, client_address = command_socket.accept()
    print(f"New connection from {client_address[0]}:{client_address[1]}")

    handle_command(client_socket, client_address)
