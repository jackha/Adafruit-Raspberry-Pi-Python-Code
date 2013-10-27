import socket
import sys

import threading
import datetime
import time

from server import server

# make ctrl-c kill the program
import signal 
import sys
def signal_handler(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



class Communication():
    def __init__(self, sock, *args, **kwargs):
        self.sock = sock

    def set(self, message):
        print 'echo %s' % message
        sock.sendall(message)  # echo all messages


class ServerThread(threading.Thread):
    def __init__(self, communication, *args, **kwargs):
        self.communication = communication
        super(ServerThread, self).__init__(*args, **kwargs)

    def run(self):
        server('localhost', 3001, communication=self.communication)


if __name__ == '__main__':
    # Create a socket (SOCK_STREAM means a TCP socket)
    # client of puredata: use 'netreceive 3000' in pd
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 3000))

    communication = Communication(sock=sock)
    server_thread = ServerThread(communication=communication)
    server_thread.daemon = True
    server_thread.start()

    sock.sendall('0;')

    # TODO: handle events from input device
    while True:
        time.sleep(1)

