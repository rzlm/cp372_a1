"""
File: Server.py
Authors: Razan Mohamed, Mahrosh Chaudry
"""
import socket
import sys
import threading
import datetime
import os

maxClients = 3
client_counter = 0
clientCache = []    # Cache of clients that have connected

def get_current_formatted_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def list_files_in_directory():  
    # List all files in the current directory
    files = os.listdir("repository")    
    for file in files:
        print(file)
    return files

def send_file_to_client(client_socket, file_name):
    try:
        with open(f"repository/{file_name}", "rb") as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)
            print(f"File {file_name} sent successfully.")
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        client_socket.send("File not found".encode())



def handle_client(client_socket, addr, client_name):
    global clientCache
    global client_counter
    while True:
        try:
            data = client_socket.recv(1024).decode() #recieves 1024 bytes of data and decodes to string
            if not data:
                break
            if data.lower() == 'exit':
                #add disconnection time to cache
                print(f"Connection from {client_name} ({addr}) closed.")
                clientCache.append(f"Client Name: {client_name}  Connection closed at {get_current_formatted_time()} ")
                client_counter -= 1
                client_socket.send("exit ACK".encode())
                client_socket.close()
                
                break
            elif data.lower() == 'status':
                cache_string = "\n".join(clientCache)
                client_socket.send(cache_string.encode())
                #print cache
                print("Client Cache:")
                for i in clientCache:
                    print(i)
                continue
            elif data.lower() == 'list':
                files = list_files_in_directory()
                files_string = "\n".join(files)
                client_socket.send(files_string.encode())
                #request file from client
                file_name = client_socket.recv(1024).decode()
                send_file_to_client(client_socket, file_name)
                continue
            print(f"Received from {client_name} ({addr}): {data} ACK")
            modified_data = data + " ACK"
            client_socket.send(modified_data.encode())
        except:
            break #if an error occurs, stop the loop so no issues
        
            

def start_server():
    global clientCache
    global client_counter
    global client_number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(0)
    print("Server is listening...")

    while True:
        try:
          #  if(client_counter < maxClients):
            if client_counter < maxClients:

                client_socket, addr = server_socket.accept() # Accept a connection
                client_name = f"[Client {client_counter+1:02d}]"
                print(f"Connection from {client_name}. Address: {addr}")
                client_counter += 1 

                client_socket.send(client_name.encode())
                    #add client to cache
                clientCache.append(f"Client Name: {client_name}  Connection accepted at {get_current_formatted_time()} ")
                client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, client_name))
                client_handler.start()
        #   else:
        #     print("Max number of clients reached")
            
        except Exception as e:
            print(f"Error: {e}")
            break
        except KeyboardInterrupt:
            print("Server shutting down...")
            server_socket.close()
            sys.exit()  # Exit the program
           

if __name__ == '__main__':
    start_server()