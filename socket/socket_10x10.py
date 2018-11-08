"""

Cenário: comunicação de dez processos com um processo via socket

Origem: processo que escreve
Destino: processo que lê

10 processo origem enviam, cada um para outro 1 processo destino distinto,
totalizando 10 processos destino, que recebem pacote e exibem as respectivas mensagens

"""

from multiprocessing import Process
from os import getpid
from socket import socket, AF_INET, SOCK_STREAM

# Envia dados para processo destino via socket, com porta definida previamente
def cliente(porta):
    # Define ip para conexão e mensagem a ser enviada
    ip = 'localhost'
    mensagem = "\"Saudações do processo %s!\"" % getpid()

    # Cria socket tcp
    with socket(AF_INET, SOCK_STREAM) as s:
        # Conecta o socket ao endereço dado pelo ip e porta
        s.connect((ip, porta))

        # Envia a mensagem através do socket
        s.send(mensagem.encode())

# Recebe dados do processo origem via socket, com porta definida previamente
def servidor(porta):
    # Define ip para conexão e tamanho do buffer em bytes
    ip = 'localhost'
    buffer = 1024

    # Cria socket tcp
    with socket(AF_INET, SOCK_STREAM) as s:
        # Atrela o socket ao ip e porta definidos
        s.bind((ip, porta))

        # Permite que o servidor aceite 1 conexão
        s.listen(1)

        # Aceita uma conexão e recebe um objeto usado para receber e enviar dados
        conexao, _ = s.accept()
        with conexao:
            while True:
                # Recebe dados em bytes do socket, de tamanho máximo 1024
                mensagem = conexao.recv(buffer)

                # Quando não houver mais o que receber, sai do loop e acaba a conexão
                if not mensagem:
                    break
                
                # Exibe no terminal o pid do processo destino e a mensagem recebida
                print("Processo %s recebeu: %s" % (getpid(), mensagem.decode()))

# Realiza a comunicação via socket de 10 processos com
# outros 10 processos (1 para cada processo que envia mensagem)
def main():
    # Cria processos e atribui a cada um a função que executarão e a porta para conexão,
    # onde cada par de processos origem e destino se comunicarão, totalizando 10 sockets
    origem = []
    for porta in range(54321, 54331):
        p = Process(target=cliente, args=(porta,))
        origem.append(p)

    destino = []
    for porta in range(54321, 54331):
        p = Process(target=servidor, args=(porta,))
        destino.append(p)

    # Inicia a execução dos processos e faz processo pai aguardar o término de execução dos mesmos
    # Processo destino executa primeiro, já que, inicialmente, ele aguarda a requisição do cliente
    for p in destino:
        p.start()

    for p in origem:
        p.start()
        p.join()

    for p in destino:
        p.join()

if __name__ == '__main__':
    main()