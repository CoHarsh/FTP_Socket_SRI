import socket
import threading

ENCODE='utf-8'
DECODE='utf-8'

def handle_stor(conn,path):
    pass

def handle_command(conn, addr,data_addr,data_conn):
    PACKET_SIZE = 1024
    response = '220 Connection established\r\n'
    conn.send(response.encode(ENCODE))

    while True:
        command = conn.recv(PACKET_SIZE).decode(DECODE).strip()
        if not command:
            break

        command_parts = command.split()
        command_name = command_parts[0].upper()
        arguments = command_parts[1:]

        # handle diff commands
        if command_name == 'USER':
            response = '331 User name okay, need password\r\n'
        elif command_name == 'PASS':
            response = '230 User logged in, proceed\r\n'
            conn.send(response.encode(ENCODE))
        elif command_name == 'STOR':
            if(len(arguments) != 1):
                response = "501 Syntax error in parameters or arguments\r\n"
                response.send(response.encode(ENCODE))
            else: 
                file_path = arguments[0]
                handle_data(data_conn, data_addr, file_path, 'STOR')
                response = '226 Closing data connection. Requested file action successful\r\n'
                conn.send(response.encode(ENCODE))
        elif command_name == 'RETR':
            if(len(arguments) != 1):
                response = "501 Syntax error in parameters or arguments\r\n"
                response.send(response.encode(ENCODE))
            else:
                file_path = arguments[0]
                handle_data(data_conn, data_addr, file_path, 'RETR')
                response = '226 Closing data connection. Requested file action successful\r\n'
                conn.send(response.encode(ENCODE))
        else :
            response = '500 Syntax error, command unrecognized\r\n'
            conn.send(response.encode(ENCODE))
        data_conn.close()
        conn.close()



def handle_data(conn, addr, file_path, mode):
    PACKET_SIZE = 1024
    if(mode == 'STOR'):
        try:
            file = open(file_path, 'wb')
            while True:
                data = conn.recv(PACKET_SIZE)
                if not data:
                    break
                file.write(data)
            file.close()
            print("[SUCCESS]File saved")
            conn.send("File saved msg from datachannel".encode(ENCODE))
        except:
            print("[ERROR]File not saved")
            conn.send("File not saved".encode(ENCODE))
            
    elif(mode == 'RETR'):
        try:
            file = open(file_path, 'rb')
            while True:
                data = file.read(PACKET_SIZE)
                if not data:
                    break
                conn.send(data)
            file.close()
            print("[SUCCESS]File sent")
            conn.send("File sent".encode(ENCODE))
        except:
            print("[ERROR]File not sent")
            conn.send("File not sent".encode(ENCODE))     
    else:
        print("[ERROR]Invalid mode")
        conn.send("Invalid mode".encode(ENCODE))
    

def run_ftp_server():
    HOST = 'localhost'
    COMM_PORT = 21
    DATA_PORT = 20
    #create command channel
    comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    comm_sock.bind((HOST, COMM_PORT))
    comm_sock.listen(1)

    print('FTP server is running on port %d' % COMM_PORT)

    # accept commands from client
    while True:
        command_conn,command_addr = comm_sock.accept()
        print('Command channel Connected by', command_addr)
        command_conn.send('220 Connection established\r\n'.encode(ENCODE))

        #create data channel
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.bind((HOST, DATA_PORT))
        data_sock.listen(1)

        print('Data channel is running on port %d' % DATA_PORT)

        # accept data from client
        data_conn, data_addr = data_sock.accept()
        print('Data channel Connected by', data_addr)
        data_conn.send('220 Connection established\r\n'.encode(ENCODE))

        #start two threads to handle command and data
        command_thread = threading.Thread(target=handle_command, args=(command_conn, command_addr,data_addr,data_conn))
        data_thread = threading.Thread(target=handle_data, args=(data_conn, data_addr, '',''))

        command_thread.start()
        data_thread.start()

        command_thread.join()
        data_thread.join()

        data_conn.close()




if __name__ == '__main__':
    run_ftp_server()