#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Author : Ayesha S. Dina

import os
import socket
import threading

IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

### to handle the clients
def handle_client (conn,addr):


    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))

    while True:
        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
       
        send_data = "OK@"

        if cmd == "LOGOUT":
            break

        elif cmd == "TASK": 
            send_data += "LOGOUT from the server.\n"
            conn.send(send_data.encode(FORMAT))
        
        elif cmd == "UPLOAD":
            #opens new file within server directory
            with open("server/" + data[1],'+w') as file:
                #writes the data from the file
                file.write(data[2])
            # sends message back to client
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            files = ""
            #formats files into string
            for file in os.listdir('server/'):
                files = files + file + "@"
            #sends string of all file names within server directory
            conn.send(files.encode(FORMAT))
            del_file = 0
            #waits for client to send acceptable index
            while not del_file:
                del_file =  conn.recv(SIZE).decode(FORMAT)
            #removes file
            os.remove("server/" + del_file)
            conn.send(send_data.encode(FORMAT))





    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening
    print(f"server is listening on {IP}: {PORT}")
    while True:
        conn, addr = server.accept() ### accept a connection from a client
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()

