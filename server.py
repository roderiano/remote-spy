import socket
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from commands import ClientCommand, ServerCommand

HOST, PORT, BUFF_SIZE = '127.0.0.1', 8888, 1024


def create_socket():
    try:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as error:
        print("Socket creation error: {}".format(str(error)))


def bind_socket():
    try:
        print("Binding socket to port {}".format(str(PORT)))
        
        s.bind((HOST, PORT))
        s.listen(5) 
    except socket.error as error:
        print("Socket binding error: {}\nRetrying...".format(str(error)))
        bind_socket()


def accept_connection():
    conn, address = s.accept()
    print("Successfully connected from {}:{}".format(address[0], str(address[1])))

    with conn:
        print('Connected by', address)

        encoded_frame = b''
        while True:
            data = conn.recv(BUFF_SIZE)

            # authorizes the client to send a frame
            if data == ClientCommand.request_permission_to_send_frame:
                encoded_frame = b''
                conn.send(ServerCommand.request_authorized)

            # renders the received frame
            elif data == ClientCommand.frame_sent:
                frame = Image.open(BytesIO(base64.b64decode(encoded_frame)))

                frame_cv = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                cv2.imshow("video", frame_cv)
                k = cv2.waitKey(10) & 0XFF

            # receives frame chunk
            else:
                encoded_frame += data
                conn.send(ServerCommand.frame_chunk_received)


if __name__ == '__main__':
    create_socket()
    bind_socket()
    accept_connection()
