""" Cenário: comunicação de um processo com outro processo via pipe """

from multiprocessing import Pipe, Process
import os

# Recebe dados do processo origem
def leitura(r, w):
    w.close()               # Fecha a escrita no pipe
    mensagem = r.recv()     # Recebe mensagem
    print("Processo %s recebeu: %s" % (os.getpid(), mensagem))
    r.close()               # Fecha a leitura do pipe

# Envia dados para o processo destino
def escrita(r, w):
    r.close()               # Fecha a leitura do pipe
    mensagem = "\"Saudações do processo %s!\"" % os.getpid()
    w.send(mensagem)        # Envia mensagem
    w.close()               # Fecha a escrita no pipe

if __name__ == '__main__':
    r, w = Pipe()           # Cria pipe

    origem = Process(target=escrita, args=(r, w))
    destino = Process(target=leitura, args=(r, w))

    origem.start()          # Inicia execução dos processos
    destino.start()

    origem.join()           # Aguarda término de execução dos processos
    destino.join()