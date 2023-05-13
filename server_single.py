# import modules
import socket
import time

# define global variables
HOST = '127.0.0.1'
PORT = 2999
BUFSIZE = 1024
ADDR = (HOST, PORT)

#save the throughtput and time elapsed, filesize to csv file
def save_to_csv(file_name, file_size, time_elapsed, throughput) :
    file = open('server.csv', 'a')
    file.write("{},{},{}\n".format(file_size, time_elapsed, throughput))
    file.close()
    return

#handle client connection
def getfile_from_client(server) :
    client, addr = server.accept()
    print('connected by', addr)
    client.send('connected to server'.encode())
    # get the file name
    file_name = client.recv(BUFSIZE).decode()
    print('file name is', file_name)
    client.send("1".encode())
    # get the file size
    file_size = client.recv(BUFSIZE).decode()
    print('file size is', file_size)
    client.send("1".encode())
    # get the file content
    start_time = time.time()
    file = open(file_name, 'wb')
    print("server is receiving file...")
    byte_received = 0
    while byte_received < int(file_size) :
        file_content = client.recv(BUFSIZE)
        file.write(file_content)
        byte_received += BUFSIZE
    file.close()
    print("file received :{}".format(file_name))
    client.send("1".encode())
    end_time = time.time()
    print("time elapsed :{}".format(end_time - start_time))
    client.send(str(end_time-start_time).encode())
    throughput = int(byte_received) / (end_time - start_time)
    print("throughput :{}".format(throughput))
    client.send(str(throughput).encode())
    save_to_csv(file_name, file_size, end_time - start_time, throughput)
    client.close()
    print("connection closed")
    return
        


#handle main function
if __name__ == '__main__' :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(1)
    while True :
        print('waiting for connection...')
        getfile_from_client(server)

    # server.close()


