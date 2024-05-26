import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Connection closed by the server.")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            sys.exit()
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))

    print("Connected to the server. Type 'exit' to quit.")
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    send_messages(client_socket)
