""" Cenário: comunicação de dez processos com dez processos via socket """

from multiprocessing import Process
from os import getpid

import socket

# Execução do processo que envia a mensagem, com porta definida previamente
def cliente(porta):
    ip = 'localhost'
    mensagem = "\"Saudações do processo %s!\"" % getpid()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, porta))
        s.send(mensagem.encode())

# Execução do processo que envia a mensagem, com porta definida previamente
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
                print("Processo %s recebeu: %s" % (getpid(), mensagem.decode()))

# Execução do cenário
def main():
    # Cria 10 processos clientes e 10 processos servidores
    # Cada processo se conecta a outro através de uma porta diferente
    # Ao criar cada processo, adiciona-o à respectiva lista
    origem = []
    for porta in range(54321, 54331):
        p = Process(target=cliente, args=(porta,))
        origem.append(p)

    destino = []
    for porta in range(54321, 54331):
        p = Process(target=servidor, args=(porta,))
        destino.append(p)

    # Inicia a execução dos processos
    for p in destino + origem:
        p.start()

    # Processo principal termina sua execução apenas ao final
    # da execução de todos os processos criados
    for p in destino + origem:
        p.join()

if __name__ == '__main__':
    main()