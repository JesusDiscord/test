import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
            broadcast(message, client_socket)
        except:
            client_socket.close()
            break

def broadcast(message, current_socket):
    for client in clients:
        if client != current_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                remove(client)

def remove(client):
    if client in clients:
        clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)
clients = []

print("Server started on port 9999...")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f"Accepted connection from {addr}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
