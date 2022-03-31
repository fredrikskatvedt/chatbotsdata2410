import socket
import threading
import random
import argparse



PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []
clientconn = []
botname = []
good = ["jump", "help", "learn", "cheer", "paint", "relax"]
bad = ["swear", "fight", "attack", "threaten", "complain", "destroy"]


def broadcastmessages(message, conn):
    for i in clients:
        if i is not conn:
            i.send(message.encode(FORMAT))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        broadcastmessages(msg, conn)
        if msg == "dc":
            broadcastmessages(f'\nthe user is now disconnected from the chat room!\n'.encode(FORMAT), conn)
            # i = clients.index(conn)
            clients.remove(conn)
            connected = False
        if msg == "connect heidi":
            heidi(msg, conn)
        if msg == "connect ralf":
            ralf(msg, conn)
        msg_diced = msg.split()
        verb = ""
        i = 0
        badword = False
        goodword = False
        while i < len(msg_diced):
            if msg_diced[i] in bad and goodword is False:
                verb = msg_diced[i]
                badword = True
            if msg_diced[i] in good and badword is False:
                verb = msg_diced[i]
                goodword = True
            i += 1


        print(f"[{addr}] {msg}")
        print(verb," ", badword, " ", goodword)

def heidi(msg, conn):
    if msg == "connect heidi":
        broadcastmessages("heidi has connected to the chat room", conn)
        botname.append("heidi")
        clientconn.append(conn)


def ralf(msg, conn):
    if msg == "connect ralf":
        broadcastmessages("ralf has connected to the chat room", conn)
        botname.append("ralf")
        clientconn.append(conn)



    '''
    altAnswers = [
        "{}: I would rather cheat than go {} -".format("ralf", verb + "ing"),
        "{}: Man... {} sucks! -".format("ralf", verb + "ing"),
        "{}: I've got better things to do than {}.. -".format("ralf", verb + "ing")
    ]

    if verb in bad or verb in good:
        broadcastmessages(random.choice(altAnswers), conn)
'''

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        # broadcastmessages(f'\nA new user is now connected\n'.encode(FORMAT), conn)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        clients.append(conn)


print("[STARTING] server is starting...")
start()
