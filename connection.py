from threading import Thread
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from commands import ClientCommand, ServerCommand

BUFF_SIZE = 1024


class Connection(Thread):
    def __init__(self, conn, address):
        Thread.__init__(self)
        self.conn = conn
        self.address = address

    def run(self):
        with self.conn:
            encoded_frame = b''
            while True:
                self.conn.send(ServerCommand.request_frame)

                data = self.conn.recv(BUFF_SIZE)
                while data != ClientCommand.frame_sent:
                    self.conn.send(ServerCommand.frame_chunk_received)
                    encoded_frame += data
                    data = self.conn.recv(BUFF_SIZE)

                frame = Image.open(BytesIO(base64.b64decode(encoded_frame)))
                frame_cv = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                cv2.imshow("{}:{}".format(self.address[0], str(self.address[1])), frame_cv)
                k = cv2.waitKey(10) & 0XFF
                encoded_frame = b''
