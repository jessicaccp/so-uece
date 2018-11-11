"""

Cenario: comunicacao de um processo com outro processo via pipe

1 processo remetente escreve para outro 1 processo destinatario, que le e exibe a mensagem

"""

from multiprocessing import Pipe, Process
from os import getpid
from time import time
import psutil

# Recebe dados do processo remetente via pipe
def leitura(r, w):
    p = psutil.Process(getpid())
    # Fecha a escrita no pipe
    w.close()

    # Recebe mensagem e a exibe no terminal junto com seu PID
    t = time()
    mensagem = r.recv()
    print("Tempo de recebimento: %s" % (time() - t))
    print("Processo %s recebeu: %s" % (getpid(), mensagem))

    # Fecha a leitura do pipe
    r.close()
    print(p.memory_info())

# Envia dados para o processo destinatario via pipe
def escrita(r, w):
    p = psutil.Process(getpid())
    # Fecha a leitura do pipe
    r.close()

    # Define mensagem contendo seu PID e a envia
    mensagem = "\"Saudacoes do processo %s!\"" % getpid()
    t = time()
    w.send(mensagem)
    print("Tempo de envio: %s" % (time() - t))

    # Fecha a escrita no pipe
    w.close()
    print(p.memory_info())

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