import socket
import struct
import time
import os
import sys

# define global variables
HOST = '127.0.0.1'
PORT = 2999
BUFSIZE = 1024
ADDR = (HOST, PORT)

file_name = sys.argv[1]


def send_file_server(client) :
    print("[MESSAGE]Client is ready to connect")
    msg = client.recv(BUFSIZE).decode()
    print("[SERVER]{}".format(msg))
    file_name_server = 'server_' + file_name
    client.send(file_name_server.encode())
    msg = client.recv(BUFSIZE).decode()
    if(msg == '1') :
        print("[MESSAGE]File name is sent")
    else :
        print("[ERROR]File name is not sent")
        sys.exit()
    file_size = os.path.getsize(file_name)
    client.send(str(file_size).encode())
    msg = client.recv(BUFSIZE).decode()
    if(msg == '1') :
        print("[MESSAGE]File size is sent")
    else :
        print("[ERROR]File size is not sent")
        sys.exit()
    #open the file
    file = open(file_name, 'rb')
    print("[MESSAGE]File is opened")
    #send the file content
    start_time = time.time()
    print("[MESSAGE]Client is sending file...")
    byte_sent = 0
    while byte_sent < file_size :
        file_content = file.read(BUFSIZE)
        client.send(file_content)
        byte_sent += BUFSIZE
    file.close()
    print("[MESSAGE]File is sent")
    msg = client.recv(BUFSIZE).decode()
    if(msg == '1') :
        print("[MESSAGE]File is sent")
    else :
        print("[ERROR]File is not sent")
        sys.exit()
    end_time = time.time()
    print("[MESSAGE]Time elapsed :{}".format(end_time - start_time))
    msg = client.recv(BUFSIZE).decode()
    print("[SERVER] Time elapsed :{}".format(msg))
    msg = client.recv(BUFSIZE).decode()
    print("[SERVER] Throughput :{}".format(msg))
    return


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send_file_server(client)
    client.close()
    print("[MESSAGE]Connection closed")
    sys.exit()

    

    


