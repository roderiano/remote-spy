import socket
import threading
from connection import Connection
import re


HOST, PORT = '127.0.0.1', 8888

job = []  # [command, args]
connections = []


def manager():
    """ method responsible for run accept_connections thread, manage user input and execute local methods """

    threading.Thread(target=accept_connections,).start()

    while True:
        convert_input_to_job(input('remote-spy>'))

        if job:
            if job[0] == 'list':
                list_connections()
            elif job[0] == 'exit':
                stop_threads()
                break
            elif job[0] == 'spy':
                enable_remote_viewing()


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
    """ validates input command with regex and converts it to job """
    global job

    job_command = re.search(r'^([a-z]+)\s?(.*)$', input_string)
    if job_command:
        if job_command.group(0) in ['list', 'exit', 'spy']:
            job = [job_command.group(0), job_command.group(0).strip()]
        else:
            print('Invalid command')
    else:
        print('Invalid command syntax')


def list_connections():
    """ print all connections and reset job """

    if len(connections) > 0:
        print('\nID   ADDRESS')
        for connection in connections:
            print('{}   {}:{}'.format(str(connections.index(connection)).zfill(2),
                                      connection.address[0],
                                      str(connection.address[1])
                                      ))
        print('\n')
    else:
        print('No connections')

    job.clear()


def stop_threads():
    pass


def enable_remote_viewing():
    pass


if __name__ == '__main__':
    manager()
