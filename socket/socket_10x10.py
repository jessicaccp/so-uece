"""

Cenario: comunicacao de dez processos com um processo via socket

10 processo remetente enviam, cada um para outro 1 processo destinatario distinto,
totalizando 10 processos destinatario, que recebem pacote e exibem as respectivas mensagens

"""

from multiprocessing import Process
from os import getpid
from socket import socket, AF_INET, SOCK_STREAM
from time import time
import psutil

# Envia dados para processo destinatario via socket, com porta definida previamente
def cliente(porta):
    p = psutil.Process(getpid())
    # Define ip para conexao e mensagem a ser enviada
    ip = 'localhost'
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

# Recebe dados do processo remetente via socket, com porta definida previamente
def servidor(porta):
    p = psutil.Process(getpid())
    # Define ip para conexao e tamanho do buffer em bytes
    ip = 'localhost'
    buffer = 1024

    # Cria socket tcp
    with socket(AF_INET, SOCK_STREAM) as s:
        # Atrela o socket ao ip e porta definidos
        s.bind((ip, porta))

        # Permite que o servidor aceite 1 conexao
        s.listen(1)

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

# Realiza a comunicacao via socket de 10 processos com
# outros 10 processos (1 para cada processo que envia mensagem)
def main():
    # Cria processos e atribui a cada um a funcao que executarao e a porta para conexao,
    # onde cada par de processos remetente e destinatario se comunicarao, totalizando 10 sockets
    remetente = []
    for porta in range(54321, 54331):
        p = Process(target=cliente, args=(porta,))
        remetente.append(p)

    destinatario = []
    for porta in range(54321, 54331):
        p = Process(target=servidor, args=(porta,))
        destinatario.append(p)

    # Inicia a execucao dos processos e faz processo pai aguardar o termino de execucao dos mesmos
    # Processo destinatario executa primeiro, ja que, inicialmente, ele aguarda a requisicao do cliente
    for p in destinatario:
        p.start()

    for p in remetente:
        p.start()
        p.join()

    for p in destinatario:
        p.join()

if __name__ == '__main__':
    main()