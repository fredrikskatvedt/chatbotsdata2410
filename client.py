import socket
import threading
import argparse

parser = argparse.ArgumentParser(description="Join the chatroom by writing for example: client.py localhost 5050")
parser.add_argument("IP", type=str, help="The servers IP address the client is connecting to")
parser.add_argument("port", type=int, help="The clients port")
args = parser.parse_args()
SERVER = args.IP
PORT = args.port
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

bots = ["heidi", "truls", "ralf", "jahn"]


#prints the clients messages
def recievemessage():
    while True:
        message = client.recv(2048).decode(FORMAT)
        print(message)


#sends the message to the server
def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)


#where the user writes their messages
def messages():
    gigner = True
    while gigner:
        msg = input()
        if msg == "dc":
            print("You are now disconnected from the chat room\n")
            gigner = False

        if msg == "":
            print("You have to write something\n")
            continue
        send(msg)


messages_thread = threading.Thread(target=messages)
messages_thread.start()

receive_thread = threading.Thread(target=recievemessage)
receive_thread.start()
