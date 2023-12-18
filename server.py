import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Function to get the list of clients
def list_clients():
    client_list = ", ".join(nicknames)
    return f"Подключенные клиенты: {client_list}"


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024 * 4)
            message_str = message.decode('utf-8')
            if message_str.lower() == 'bye' or message_str.lower() == 'пока':
                index = clients.index(client)
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('utf-8'))
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                break
            elif message_str.lower() == 'кто в чате':
                client.send(list_clients().encode('utf-8'))
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


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)), 'utf-8')

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname), 'utf-8')
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server if listening...")
receive()
