import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('94.241.168.240', 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            # Close Connection When Error
            print(f"An error occurred: {e}")
            client.close()
            break


# Sending messages
def write():
    while True:
        message = input('')
        if message.lower() in ['bye', 'пока']:
            client.send(message.encode('utf-8'))
            client.close()
            break
        elif message.lower() == 'кто в чате':
            client.send(message.encode('utf-8'))
        else:
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
