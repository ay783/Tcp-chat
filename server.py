import threading
import socket

host = '127.0.0.1'
port = 55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []


def boardcast(message):
    for clinet in clients:
        clinet.send(message)


def handle_clinet(client):
    while True:
        try:
            message = client.recv(1024)
            boardcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            boardcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break


# Main function to receive the clients connection

def receive():
    while True:
        print('Server is running and listening.....')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))

        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)

        print(f'The alias of the client is {alias}')
        boardcast(f'{alias} has connected to chat room'.encode('utf-8'))
        client.send('you are now connected'.encode('utf-8'))

        thread= threading.Thread(target=handle_clinet,args=(client,))
        thread.start()


if _name== "__main_":
    receive()

