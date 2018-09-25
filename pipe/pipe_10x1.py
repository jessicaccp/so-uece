""" Cenário: comunicação de dez processos com um processo via pipe """

from multiprocessing import Pipe, Process, Lock
import os

# Recebe dados do processo origem
def leitura(r, w, lock):
    w.close()               # Fecha a escrita no pipe
    for _ in range(10):
        lock.acquire()
        mensagem = r.recv()     # Recebe mensagem
        print("Processo %s recebeu: %s" % (os.getpid(), mensagem))
        lock.release()
    r.close()               # Fecha a leitura do pipe

# Envia dados para o processo destino
def escrita(r, w, lock):
    r.close()               # Fecha a leitura do pipe
    lock.acquire()
    mensagem = "\"Saudações do processo %s!\"" % os.getpid()
    w.send(mensagem)        # Envia mensagem
    lock.release()
    w.close()               # Fecha a escrita no pipe

if __name__ == '__main__':
    r, w = Pipe()           # Cria pipe
    lock = Lock()

    origem = []
    for _ in range(10):
        p = Process(target=escrita, args=(r, w, lock))
        origem.append(p)
    
    destino = Process(target=leitura, args=(r, w, lock))

    for p in origem:
        p.start()           # Inicia execução dos processos
    destino.start()

    for p in origem:
        p.join()           # Aguarda término de execução dos processos
    destino.join()