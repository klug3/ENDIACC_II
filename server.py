import threading
import socket

host = "endiacc.projektstudencki.pl"  # server adress
port = 8282  # opened port (i.e. <PORT2>)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def bradcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)
        if client == sender and message[:9].decode("utf-8") == "!COMMAND_":
            client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            bradcast(message, sender=client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            bradcast(f">>{nickname} left the chat.".encode("utf-8"), sender=client)
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, adress = server.accept()
        print(f"Connected with (str{adress})")

        client.send("!NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the clint is {nickname}!")
        bradcast(f">>{nickname} joined the chat!".encode("utf-8"), sender=client)
        client.send(">>Connected to the server!".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
