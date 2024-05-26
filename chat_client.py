import socket
import threading
import sys
import os
from colorama import Fore, init
from dotenv import load_dotenv

load_dotenv()
init(autoreset=True)

SERVER = os.getenv("CHAT_SERVER_HOST", "127.0.0.1")
PORT = int(os.getenv("CHAT_SERVER_PORT", 9999))
PASSWORD = os.getenv("CHAT_PASSWORD", "secret_password")

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
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
            sys.exit()
        client_socket.send(message.encode('utf-8'))

def connect_to_server(server, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server, port))
        client_socket.send(PASSWORD.encode('utf-8'))
        auth_response = client_socket.recv(1024).decode('utf-8')
        if "Authentication failed!" in auth_response:
            print(auth_response)
            client_socket.close()
            return None
        print(auth_response)
        username = input("Enter your username: ")
        client_socket.send(username.encode('utf-8'))
        
        print(f"Connected to {server} on port {port}. Type 'exit' to quit.")
        
        threading.Thread(target=receive_messages, args=(client_socket,)).start()
        send_messages(client_socket)
    except Exception as e:
        print(f"Unable to connect to {server} on port {port}: {e}")

def main():
    connect_to_server(SERVER, PORT)

if __name__ == "__main__":
    main()
