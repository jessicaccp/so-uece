""" Cenário: comunicação de um processo com outro processo via socket """

from multiprocessing import Process
from os import getpid

import socket

# Execução do processo que envia a mensagem
def cliente():
    # Define ip e porta para conexão e mensagem a ser enviada
    ip = 'localhost'
    porta = 54321
    mensagem = "\"Saudações do processo %s!\"" % getpid()

    # Cria socket tcp
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conecta o socket ao endereço dado pelo ip e porta
        s.connect((ip, porta))
        # Envia a mensagem através do socket
        s.send(mensagem.encode())

# Execução do processo que recebe a mensagem
def servidor():
    # Define ip e porta para conexão e tamanho do buffer em bytes
    ip = 'localhost'
    porta = 54321
    buffer = 1024

    # Cria socket tcp
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Liga o socket no ip e porta definidos
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

# Execução do cenário
def main():
    # Cria dois processos
    ## origem: o que envia a mensagem e executa a função cliente()
    ## destino: o que recebe a mensagem e executa a função servidor()
    origem = Process(target=cliente)
    destino = Process(target=servidor)

    # Inicia a execução dos processos
    ## Processo destino executa primeiro, já que ele aguarda a requisição do cliente
    destino.start()
    origem.start()

    # Processo principal aguarda que os processos criados terminem suas execuções
    ## Impede que o programa termine antes que os processos sejam finalizados
    origem.join()
    destino.join()

if __name__ == '__main__':
    main()