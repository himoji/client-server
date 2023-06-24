import socket 


HEADER_SIZE = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONECT_MESSAGE = "!DISCONNECT"
MSG_RECEIVED = "!MSG_RECEIVED"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_message() -> str:
    """Receives a message\n
    Returns:
        str: {MSG_RECEIVED}   
    """
    msg_len = int(client.recv(HEADER_SIZE).decode(FORMAT))
    msg = client.recv(msg_len).decode(FORMAT)
    return msg

def send_message(msg):
    message_to_send = msg.encode(FORMAT)
    msg_len = len(message_to_send)

    send_len = str(msg_len).encode(FORMAT)
    send_len += b" " * (HEADER_SIZE - len(send_len))

    client.send(send_len)
    client.send(message_to_send)

    if receive_message() == MSG_RECEIVED:
        print("Message sent and received successfully")



def disconnect():
    send_message(DISCONECT_MESSAGE)

send_message(input("Enter message: "))
disconnect()