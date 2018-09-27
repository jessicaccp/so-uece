""" Cenário: comunicação de dez processo com um processo via socket """

import socket, os
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
        # Permite que o servidor aceite 10 conexões
        s.listen(10)

        # Usa um loop para executar as conexões dos 10 processos clientes
        for _ in range(10):
            conexao, _ = s.accept()
            with conexao:
                while True:
                    mensagem = conexao.recv(buffer)
                    if not mensagem:
                        break
                    print("Processo %s recebeu: %s" % (os.getpid(), mensagem.decode()))

# Execução do cenário
def main():
    # Cria 10 processos clientes, que se conectarão ao processo servidor
    # Ao criar cada processo, adiciona-o na lista origem[]
    origem = []
    for _ in range(10):
        p = Process(target=cliente)
        origem.append(p)

    destino = Process(target=servidor)

    # Inicia a execução dos processos
    destino.start()
    for p in origem:
        p.start()

    # Processo principal termina de executar apenas ao final
    # da execução de todos os processos criados
    for p in origem:
        p.join()
    destino.join()

if __name__ == '__main__':
    main()