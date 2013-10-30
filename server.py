import socket
from time import sleep

BUFFER_SIZE = 100  # Normally 1024, but we want fast response

def server(host, port, communication=None): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
     
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print "received data:", data
        try:  
            communication.set(data.strip('\n'))
        except AttributeError:
            print "communcation object has no attribute 'set'"
            pass
        sleep(0.01)

    conn.close()

if __name__ == '__main__':
    print "serving localhost:3001..."
    server('localhost', 3001)