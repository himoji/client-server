import socket 
import threading

HEADER_SIZE = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"
MSG_RECEIVED = "!MSG_RECEIVED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send_message(connection, msg):
    message_to_send = msg.encode(FORMAT)
    msg_len = len(message_to_send)

    send_len = str(msg_len).encode(FORMAT)
    send_len += b" " * (HEADER_SIZE - len(send_len))

    connection.send(send_len)
    connection.send(message_to_send)

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address}  connected")

    connected = True 
    while connected:
        msg_len = connection.recv(HEADER_SIZE).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)

            msg = connection.recv(msg_len).decode(FORMAT)

            if msg == DISCONECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTED] {address} disconnected")
                break
            print(f"[RECEIVED] {address}: {msg}")
            send_message(connection, MSG_RECEIVED)

    connection.close()

def start():
    server.listen(1)
    print(f"[LISTEN] Listening server on {SERVER} on port {PORT}")

    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE] {threading.active_count() - 1}")

print(f"[START] starting server on {SERVER} on port {PORT}")
start()
