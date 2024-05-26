import socket
import threading
import os
import random
from colorama import Fore, init
from dotenv import load_dotenv

load_dotenv()
init(autoreset=True)

PASSWORD = os.getenv("CHAT_PASSWORD", "secret_password")
HOST = os.getenv("CHAT_SERVER_HOST", "0.0.0.0")
START_PORT = int(os.getenv("CHAT_SERVER_PORT", 9999))

COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
clients = {}
usernames_colors = {}

def handle_client(client_socket, addr):
    client_socket.send("PASSWORD:".encode('utf-8'))
    password = client_socket.recv(1024).decode('utf-8')
    if password != PASSWORD:
        client_socket.send("Authentication failed!".encode('utf-8'))
        client_socket.close()
        return
    
    client_socket.send("Authenticated successfully! Enter your username:".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')

    color = random.choice(COLORS)
    usernames_colors[username] = color

    welcome_message = f"{username} has joined the chat."
    print(welcome_message)
    broadcast(welcome_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'exit':
                disconnect_message = f"{username} has left the chat."
                print(disconnect_message)
                broadcast(disconnect_message, client_socket)
                client_socket.close()
                remove(client_socket)
                break
            full_message = f"{color}{username}: {message}{Fore.RESET}"
            print(full_message)
            broadcast(full_message, client_socket)
        except:
            client_socket.close()
            break

def broadcast(message, current_socket):
    for client in clients.values():
        if client != current_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                remove(client)

def remove(client):
    for username, client_socket in clients.items():
        if client_socket == client:
            del clients[username]
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = START_PORT
    while True:
        try:
            server.bind((HOST, port))
            print(f"Server started on {HOST}:{port}...")
            break
        except socket.error as e:
            print(f"Port {port} is in use, trying next port...")
            port += 1

    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        clients[addr] = client_socket
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
