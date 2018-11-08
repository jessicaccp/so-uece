"""

Cenário: comunicação de dez processos com um processo via socket

Origem: processo que escreve
Destino: processo que lê

10 processo origem enviam e outro 1 processo destino recebe pacotes, exibindo as mensagens em seguida

"""

from multiprocessing import Process
from os import getpid
from socket import socket, AF_INET, SOCK_STREAM

# Envia dados para processo destino via socket
def cliente():
    # Define ip e porta para conexão e mensagem a ser enviada
    ip = 'localhost'
    porta = 54321
    mensagem = "\"Saudações do processo %s!\"" % getpid()

    # Cria socket tcp
    with socket(AF_INET, SOCK_STREAM) as s:
        # Conecta o socket ao endereço dado pelo ip e porta
        s.connect((ip, porta))

        # Envia a mensagem através do socket
        s.send(mensagem.encode())

# Recebe dados do processo origem via socket
def servidor():
    # Define ip e porta para conexão e tamanho do buffer em bytes
    ip = 'localhost'
    porta = 54321
    buffer = 1024

    # Cria socket tcp
    with socket(AF_INET, SOCK_STREAM) as s:
        # Atrela o socket ao ip e porta definidos
        s.bind((ip, porta))

        # Permite que o servidor aceite 10 conexões
        s.listen(10)

        # Usa um loop para executar as conexões dos 10 processos clientes
        for _ in range(10):
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

# Realiza a comunicação via socket de 10 processos com outro processo
def main():
    # Cria processos e atribui a cada um a função que executarão
    origem = []
    for _ in range(10):
        p = Process(target=cliente)
        origem.append(p)

    destino = Process(target=servidor)

    # Inicia a execução dos processos e faz processo pai aguardar o término de execução dos mesmos
    # Processo destino executa primeiro, já que, inicialmente, ele aguarda a requisição do cliente
    destino.start()

    for p in origem:
        p.start()
        p.join()

    destino.join()

if __name__ == '__main__':
    main()