import socket, os, time
from multiprocessing import Process

def cliente():
    ip = 'localhost'
    porta = 54321
    mensagem = "\"Saudações do processo %s!\"" % os.getpid()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, porta))
        s.send(mensagem.encode())

def servidor():
    ip = 'localhost'
    porta = 54321
    buffer = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, porta))
        s.listen(10)

        for _ in range(10):
            conexao, _ = s.accept()
            with conexao:
                while True:
                    mensagem = conexao.recv(buffer)
                    if not mensagem:
                        break
                    print("Processo %s recebeu: %s" % (os.getpid(), mensagem.decode()))

if __name__ == '__main__':
    origem = []
    for _ in range(10):
        p = Process(target=cliente)
        origem.append(p)

    destino = Process(target=servidor)

    destino.start()
    for p in origem:
        p.start()

    for p in origem:
        p.join()
    destino.join()