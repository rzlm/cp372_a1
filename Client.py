"""
File: Client.py
Authors: Razan Mohamed, Mahrosh Chaudry
"""
import socket

def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))  # Connect to the server

        client_name = client_socket.recv(1024).decode()
        print(f"Client name: {client_name}")

        while True:
            message = input("Enter message to send: ")
            if message.lower() == 'exit': # end the loop if the user wants to exit
                client_socket.send(message.encode())
                break
            elif message.lower() == 'status': # print the cache
                #get the chace from the server
                client_socket.send(message.encode())
                clientCache = client_socket.recv(1024).decode()
                print("Client Cache:")
                print(clientCache)
                
                continue
            client_socket.send(message.encode())
            
            data = client_socket.recv(1024).decode()
            print(f"Received from server: {data}")

        print("close the connection")
        client_socket.close()
    except ConnectionRefusedError:
        print("Cannot connect to the server.")
        client_socket.close()
    except KeyboardInterrupt:
        print("Exiting...")
        client_socket.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        client_socket.close()


    

if __name__ == '__main__':
    start_client()
