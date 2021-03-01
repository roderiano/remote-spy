import socket
import threading
from connection import Connection
import re


HOST, PORT = '127.0.0.1', 8888

job = {}
connections = []


def manager():
    """" method responsible for run accept_connections thread, manage user input and execute local methods """

    global job
    threading.Thread(target=accept_connections,).start()

    while True:
        try:
            job = parse_input_to_job(input('remote-spy>'))

            if job:
                if job['command'] == 'list':
                    list_connections()
                elif job['command'] == 'exit':
                    stop_threads()
                    break
                elif job['command'] == 'spy':
                    enable_remote_viewing()
        except Exception as error:
            print("{}: {}".format(type(error).__name__, str(error)))


def accept_connections():
    """" accept connections and run as thread """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        conn, address = s.accept()
        connection_thread = Connection(conn, address)
        connection_thread.start()
        connections.append(connection_thread)


def parse_input_to_job(input_string):
    """" validates input and parse it to job """

    global job

    match = re.search(r'^([a-z]+)\s?(.*)$', input_string)
    if match:
        """" get command and args """
        args = []
        command = match.group(1)
        match_args = match.group(2).strip().split(' ')

        if match_args[0] == '':
            match_args.remove('')

        """" set arg validators """
        if command == 'spy':
            arg_validators = [{'arg_name': 'ip', 'required': True}]
        elif command in ['list', 'exit']:
            arg_validators = None
        else:
            raise SyntaxError('Invalid command "{}"'.format(command))

        """" validate args """
        if arg_validators is not None:
            for validator in arg_validators:
                validated = False

                for match_arg in match_args:

                    """" remove validated arg """
                    if validated:
                        match_args.remove(match_arg)
                        match_args.remove(validator['arg_name'])
                        break

                    """" validate arg """
                    arg_attribute_idx = match_args.index(match_arg) + 1
                    if match_arg == validator['arg_name']:
                        if arg_attribute_idx > len(match_args) - 1:
                            raise ValueError('Command "{}" requires arg "{}" attribute'.format(command, match_arg))

                        args.append({validator['arg_name']: match_args[arg_attribute_idx]})
                        validated = True

                """" raise exceptions """
                if len(match_args) > 0:
                    raise NameError('"{}" is an invalid arg name'.format(match_args[0]))
                elif not validated and validator['required']:
                    raise SyntaxError('Arg "{}" is required'.format(validator['arg_name']))
        elif len(match_args) > 0:
            raise ValueError('"{}" command takes no args'.format(command))

        return {'command': command, 'args': args}
    else:
        raise SyntaxError('Invalid command syntax')


def list_connections():
    """" print all connections and reset job """

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
