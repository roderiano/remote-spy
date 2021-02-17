import socket
import threading
from connection import Connection
import re

HOST, PORT = '127.0.0.1', 8888

job = []
connections = []


def manager():
    """ method responsible for manage user input and run accept_connections thread """

    threading.Thread(target=accept_connections,).start()

    while True:
        convert_input_to_job(input('remote-spy>'))

        if job:
            if job[0] == 'list':
                list_connections()


def accept_connections():
    """ accept connections and run as thread """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        conn, address = s.accept()
        connection_thread = Connection(conn, address)
        connection_thread.start()
        connections.append(connection_thread)


def convert_input_to_job(input_string):
    """ validates input with regex and converts it to job """
    global job

    job_command = re.search(r'^([a-z]+)$', input_string)
    if job_command:
        if job_command.group(0) in ['list', ]:
            job = ['list', '']
        else:
            print('Invalid command')
    else:
        print('Invalid command syntax')


def list_connections():
    """ print all connections and reset job """
    global job

    print('\nID   ADDRESS')
    for connection in connections:
        print('{}   {}:{}'.format(str(connections.index(connection)).zfill(2),
                                  connection.address[0],
                                  str(connection.address[1])
                                  ))

    job = []


if __name__ == '__main__':
    manager()

