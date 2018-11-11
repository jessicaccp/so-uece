"""

Cenario: comunicacao de um processo com outro processo via pipe

1 processo remetente escreve para outro 1 processo destinatario, que le e exibe a mensagem

"""

from multiprocessing import Pipe, Process
from os import getpid

# Recebe dados do processo remetente via pipe
def leitura(r, w):
    # Fecha a escrita no pipe
    w.close()

    # Recebe mensagem e a exibe no terminal junto com seu PID
    mensagem = r.recv()
    print("Processo %s recebeu: %s" % (getpid(), mensagem))

    # Fecha a leitura do pipe
    r.close()

# Envia dados para o processo destinatario via pipe
def escrita(r, w):
    # Fecha a leitura do pipe
    r.close()

    # Define mensagem contendo seu PID e a envia
    mensagem = "\"Saudacoes do processo %s!\"" % getpid()
    w.send(mensagem)

    # Fecha a escrita no pipe
    w.close()

# Realiza a comunicacao via pipe entre os dois processos
def main():
    # Cria pipe
    r, w = Pipe()

    # Cria processos e atribui a cada um a funcao que executarao
    remetente = Process(target=escrita, args=(r, w))
    destinatario = Process(target=leitura, args=(r, w))

    # Inicia a execucao dos processos e faz processo pai aguardar o termino de execucao dos mesmos
    remetente.start()
    remetente.join()

    destinatario.start()
    destinatario.join()

if __name__ == '__main__':
    main()