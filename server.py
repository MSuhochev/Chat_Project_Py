import socket
import threading

# Connection Data
host = '94.241.168.240'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Flag to control server running status
server_running = True


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            message_str = message.decode('utf-8')
            if message_str.lower() == 'стоп':
                stop_server()
                break
            elif message_str.lower() == 'кто в чате':
                send_clients_list(client)
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


# Function to send the list of clients to a specific client
def send_clients_list(client):
    client_list = ", ".join(nicknames)
    client.send(f"Подключенные клиенты: {client_list}".encode('utf-8'))


# Receiving / Listening Function
def receive():
    while server_running:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def stop_server():
    global server_running
    server_running = False
    print("Server is stopping...")
    for client in clients:
        client.send("Server is stopping...".encode('utf-8'))
        client.close()
    server.close()


print("Server is listening...")
receive()
