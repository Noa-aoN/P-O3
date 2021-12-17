import socket
import threading
from carddispencer_functies import setup, dcmotor_rotate, servo_rotate , servo_rotate_fromto


HEADER = 64
PORT = 5050
SERVER = "172.20.10.13"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)           
            if msg == DISCONNECT_MESSAGE:
                connected = False
            if msg == "GIVE CARD":
                dcmotor_rotate()
            elif "ROTATE" in msg:
                lst = msg.split()
                if len(lst) == 2:
                    print(float(lst[-1]))
                    servo_rotate(float(lst[-1]))
                elif len(lst) == 3:
                    print(float(lst[-2]),float(lst[-1]))
                    servo_rotate_fromto(float(lst[-2]),float(lst[-1]))

            print(f"[{addr}] {msg}")
            conn.send(msg.encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()