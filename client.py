import socket

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
        filename = "downloaded_" + command.split()[1]
        with open('client_side/'+filename, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if data == b'EOF':
                    break
                file.write(data)
        print(f"Finished downloading {filename}")

    if command.startswith(COMMAND_UPLOAD):
        #UPLOAD <filename> 
        new_command = "UPLOAD" + " " + "uploaded_" + command.split()[1]
        client_socket.sendall(new_command.encode())
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
            client_socket.sendall(b'EOF')
        except FileNotFoundError:
            print(f"File not found: {filename}") 

    client_socket.close()

# Client interaction loop
while True:
    # make below print more readable
    user_input = input("Enter a command \nLIST : List all the directories in server side, \nDOWNLOAD <filename> : Download the file from server, \nUPLOAD <filename> <serversidefilename> : Upload the file to server \n")
    if user_input == 'QUIT':
        break

    send_command(user_input)
