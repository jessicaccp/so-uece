"""

Cenario: comunicacao de dez processos com um processo via socket

10 processo remetente enviam e outro 1 processo destinatario recebe pacotes, exibindo as mensagens em seguida

"""

from multiprocessing import Process
from os import getpid
from socket import socket, AF_INET, SOCK_STREAM
from time import time
import psutil

# Envia dados para processo destinatario via socket
def cliente():
    p = psutil.Process(getpid())
    # Define ip e porta para conexao e mensagem a ser enviada
    ip = 'localhost'
    porta = 54321
    mensagem = "\"Saudacoes do processo %s!\"" % getpid()

    # Cria socket tcp
    with socket(AF_INET, SOCK_STREAM) as s:
        t = time()
        # Conecta o socket ao endereco dado pelo ip e porta
        s.connect((ip, porta))

        # Envia a mensagem atraves do socket
        s.send(mensagem.encode())
        print("Tempo de envio: %s" % (time() - t))
    print(p.memory_info())

# Recebe dados do processo remetente via socket
def servidor():
    p = psutil.Process(getpid())
    # Define ip e porta para conexao e tamanho do buffer em bytes
    ip = 'localhost'
    porta = 54321
    buffer = 1024

    # Cria socket tcp
    with socket(AF_INET, SOCK_STREAM) as s:
        # Atrela o socket ao ip e porta definidos
        s.bind((ip, porta))

        # Permite que o servidor aceite 10 conexoes
        s.listen(10)

        # Usa um loop para executar as conexoes dos 10 processos clientes
        for _ in range(10):
            t = time()
            # Aceita uma conexao e recebe um objeto usado para receber e enviar dados
            conexao, _ = s.accept()
            with conexao:
                while True:
                    # Recebe dados em bytes do socket, de tamanho maximo 1024
                    mensagem = conexao.recv(buffer)

                    # Quando nao houver mais o que receber, sai do loop e acaba a conexao
                    if not mensagem:
                        print("Tempo de recebimento: %s" % (time() - t))
                        break
                    
                    # Exibe no terminal o pid do processo destinatario e a mensagem recebida
                    print("Processo %s recebeu: %s" % (getpid(), mensagem.decode()))
    print(p.memory_info())

# Realiza a comunicacao via socket de 10 processos com outro processo
def main():
    # Cria processos e atribui a cada um a funcao que executarao
    remetente = []
    for _ in range(10):
        p = Process(target=cliente)
        remetente.append(p)

    destinatario = Process(target=servidor)

    # Inicia a execucao dos processos e faz processo pai aguardar o termino de execucao dos mesmos
    # Processo destinatario executa primeiro, ja que, inicialmente, ele aguarda a requisicao do cliente
    destinatario.start()

    for p in remetente:
        p.start()
        p.join()

    destinatario.join()

if __name__ == '__main__':
    main()