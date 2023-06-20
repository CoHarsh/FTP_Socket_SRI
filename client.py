import socket
import os

# Client configuration
SERVER_HOST = '127.0.0.1'
COMMAND_PORT = 12345
DATA_PORT = 12346  # Port for data channel

# Command constants
COMMAND_LIST = 'LIST'
COMMAND_DOWNLOAD = 'DOWNLOAD'
COMMAND_UPLOAD = 'UPLOAD'

def send_command(command):
    command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command_socket.connect((SERVER_HOST, COMMAND_PORT))

    if command == COMMAND_LIST:
        # LIST
        command_socket.sendall(command.encode())
        file_list = command_socket.recv(1024).decode()
        if file_list == 'EOF':
            print("Server-side directory is empty")
            return
        print(file_list)

    if command.startswith(COMMAND_DOWNLOAD):
        # DOWNLOAD <filename>
        command_socket.sendall(command.encode())
        # Check if file name is provided
        if len(command.split()) < 2:
            print("Please provide a file name")
            return
        filename = "downloaded_" + command.split()[1]

        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((SERVER_HOST, DATA_PORT))

        file_sz = int(data_socket.recv(1024).decode())
        with open('client_side/' + filename, 'wb') as file:
            while file_sz > 0:
                data = data_socket.recv(1024)
                file.write(data)
                file_sz -= len(data)
        print(f"Finished downloading {filename}")
        data_socket.close()

    if command.startswith(COMMAND_UPLOAD):
        # UPLOAD <filename>
        if len(command.split()) < 2:
            print("Please provide a file name")
            return
        new_command = "UPLOAD" + " " + "uploaded_" + command.split()[1]
        # Check if the file exists or not in the current directory
        if command.split()[1] not in os.listdir('.'):
            print(f"File not found: {command.split()[1]}")
            return

        command_socket.sendall(new_command.encode())
        file_sz = os.path.getsize(command.split()[1])
        print("File size:", file_sz, "bytes")
        command_socket.sendall(str(file_sz).encode())
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((SERVER_HOST, DATA_PORT))
        print("Uploading file to server")
        filename = command.split()[1]
        try:
            with open(filename, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    data_socket.sendall(data)
            print(f"Finished uploading {filename}")
        except FileNotFoundError:
            print(f"File not found: {filename}")
        data_socket.close()

    command_socket.close()

# Client interaction loop
while True:
    # Make the print statement more readable
    user_input = input("Enter a command \n"
                       "LIST: List all the directories in the server-side,\n"
                       "DOWNLOAD <filename>: Download the file from the server,\n"
                       "UPLOAD <filename>: Upload the file to the server\n")
    if user_input == 'QUIT':
        break

    send_command(user_input)
