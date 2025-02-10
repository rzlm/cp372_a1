"""
File: Server.py
Authors: Razan Mohamed, Mahrosh Chaudry
"""
import socket
import sys
import threading
import datetime
maxClients = 3
client_counter = 0
clientCache = []    # Cache of clients that have connected

def get_current_formatted_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

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
                clientCache.append(f"Client Name: {client_name}  Connection closed at {get_current_formatted_time()} ")
                print(f"Client count: {client_counter}")

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
            print(f"Received from {client_name} ({addr}): {data} ACK")
            modified_data = data + " ACK"
            client_socket.send(modified_data.encode())
        except:
            break #if an error occurs, stop the loop so no issues
        finally:
            print(f"Connection closed: {client_name} ({addr})")
            client_counter -= 1
            client_socket.close()
            

def start_server():
    global clientCache
    global client_counter
    global client_number
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        try:
            if(client_counter < maxClients):
                client_socket, addr = server_socket.accept() # Accept a connection
                client_name = f"[Client {client_counter+1:02d}]"
                print(f"Connection from {client_name}. Address: {addr}")

                client_number = client_counter
                client_socket.send(client_name.encode())
                client_counter += 1
                #add client to cache
                clientCache.append(f"Client Name: {client_name}  Connection accepted at {get_current_formatted_time()} ")
                client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, client_name))
                client_handler.start()
            else:
                print(f"Rejecting connection from {addr}: Server is full.")
                client_socket.send("Server is full. Try again later.".encode())  
                client_socket.close()  
                continue 
                
                
        except Exception as e:
            print(f"Error: {e}")
            break
        except KeyboardInterrupt:
            print("Server shutting down...")
            server_socket.close()
            sys.exit()  # Exit the program
           

if __name__ == '__main__':
    start_server()