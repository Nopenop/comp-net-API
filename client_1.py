# Author : Ayesha S. Dina

import os
import socket

from numpy import flexible


# IP = "192.168.1.101" #"localhost"
IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024 ## byte .. buffer size
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def main():
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    while True:  ### multiple communications
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break
        
        data = input("> ") 
        data = data.split(" ")
        cmd = data[0]

        if cmd == "TASK":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "UPLOAD":
            #Asks user for filename within client directory(folder)
            file_name = input("Filename?")
            with open("client/" + file_name,'r') as file:
                #Reads the data from the client directory
                data = file.read()
                
                #If there is no data from the file
                #Stops client
                if not data:
                    print("Error: no information in file")
                    break
                
                print("sends file")
                #sends string with command, name of file, and data from file
                client.send((cmd +"@" + file_name + "@" + str(data)).encode()) 

        elif cmd == "DELETE":
            client.send(cmd.encode(FORMAT))



    print("Disconnected from the server.")
    client.close() ## close the connection

if __name__ == "__main__":
    main()
