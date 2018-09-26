import socket, os
from multiprocessing import Process

def server():
    host = 'localhost'
    porta = 11111

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, porta))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

def client():
    host = 'localhost'
    porta = 11111

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, porta))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    print('Received', repr(data))

if __name__ == '__main__':
    origem = Process(target=client)
    destino = Process(target=server)

    destino.start()
    origem.start()

    origem.join()
    destino.join()