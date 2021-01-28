import socket
from PIL import ImageGrab
import base64
from io import BytesIO
from commands import ClientCommand, ServerCommand


HOST, PORT, BUFF_SIZE = '127.0.0.1', 8888, 1024


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        # requests authorization to send frame
        s.send(ClientCommand.request_permission_to_send_frame)
        data = s.recv(BUFF_SIZE)

        # send frame
        if data == ServerCommand.request_authorized:
            encoded_frame_chunks = get_encoded_frame()
            for chunk in encoded_frame_chunks:
                s.send(chunk)
                s.recv(1024)

            s.send(ClientCommand.frame_sent)


def get_encoded_frame():
    frame = ImageGrab.grab()
    frame_buffer = BytesIO()
    frame.save(frame_buffer, format="JPEG")

    encoded_frame = base64.b64encode(frame_buffer.getvalue())
    encoded_frame_chunks = [encoded_frame[i:i + BUFF_SIZE] for i in range(0, len(encoded_frame), BUFF_SIZE)]

    return encoded_frame_chunks


if __name__ == '__main__':
    connect()
