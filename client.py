import socket 
import os
import threading

ENCODE='utf-8'
DECODE='utf-8'
PACKET_SIZE=1024

def send_command(command,conn):
    conn.send(command.encode(ENCODE))
    response = conn.recv(PACKET_SIZE).decode(DECODE).strip()
    return response

def upload_file(file_path,host,command_port,data_port,file_name):
    #connect to command channel
    command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command_socket.connect((host, command_port))
    response = command_socket.recv(PACKET_SIZE).decode(DECODE).strip()
    print(response)

    #connect to data chennel
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((host, data_port))
    response = data_socket.recv(PACKET_SIZE).decode(DECODE).strip()
    print(response)

    #send stor command
    command = 'STOR ' + file_name + '\r\n'
    response = send_command(command,command_socket)
    print(response)

    #send file
    file = open(file_path, 'rb')
    while True:
        data = file.read(PACKET_SIZE)
        if not data:
            break
        data_socket.sendall(data)
    file.close()
    print("[SUCCESS]File sent")
    response = data_socket.recv(PACKET_SIZE).decode(DECODE).strip()
    print(response)


if __name__ == '__main__':
    HOST = '127.0.0.1'
    COMM_PORT = 21
    DATA_PORT = 20
    PACKET_SIZE = 1024
    file_path='./sample_data/resume.png'
    file_name = 'server_resume.png'
    upload_file(file_path,HOST,COMM_PORT,DATA_PORT,file_name)
    print('File uploaded')
