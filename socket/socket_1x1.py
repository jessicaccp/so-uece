import socket, os
from multiprocessing import Process

def client():
    ip = '127.0.0.1'
    porta = 54321
    mensagem = "\"Saudações do processo %s!\"" % os.getpid()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, porta))
    s.send(mensagem.encode())
    s.close()

def server():
    ip = '127.0.0.1'
    porta = 54321
    buffer = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, porta))
    s.listen(1)

    conexao, endereco = s.accept()
    with conexao:
        while True:
            mensagem = conexao.recv(buffer)
            if not mensagem:
                break
            print("Processo %s recebeu: %s" % (os.getpid(), mensagem.decode()))
        conexao.close()

if __name__ == '__main__':
    origem = Process(target=client)
    destino = Process(target=server)

    destino.start()
    origem.start()

    origem.join()
    destino.join()