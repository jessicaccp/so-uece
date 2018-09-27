import socket, os, time
from multiprocessing import Process

def cliente(porta):
    ip = 'localhost'
    mensagem = "\"Saudações do processo %s!\"" % os.getpid()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, porta))
        s.send(mensagem.encode())

def servidor(porta):
    ip = 'localhost'
    buffer = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, porta))
        s.listen(10)

        conexao, _ = s.accept()
        with conexao:
            while True:
                mensagem = conexao.recv(buffer)
                if not mensagem:
                    break
                print("Processo %s recebeu: %s" % (os.getpid(), mensagem.decode()))

if __name__ == '__main__':
    origem = []
    for porta in range(54321, 54331):
        p = Process(target=cliente, args=(porta,))
        origem.append(p)

    destino = []
    for porta in range(54321, 54331):
        p = Process(target=servidor, args=(porta,))
        destino.append(p)

    for p in destino + origem:
        p.start()

    for p in destino + origem:
        p.join()