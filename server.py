import socket
import threading
from connection import Connection

HOST, PORT = '127.0.0.1', 8888

connections = []


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print("Socket binded to port {}".format(str(PORT)))
    s.listen(5)

    while True:
        conn, address = s.accept()
        connection_thread = Connection(conn, address)
        connection_thread.start()
        connections.append(connection_thread)
        print("Successfully connected from {}:{}".format(address[0], str(address[1])))


if __name__ == '__main__':
    main()
