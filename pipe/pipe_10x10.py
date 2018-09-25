""" Cenário: comunicação de dez processos com dez processos via pipe """

from multiprocessing import Pipe, Process, Lock
import os

# Recebe dados do processo origem
def leitura(r, w, lock):
    w.close()               # Fecha a escrita no pipe
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
    
    destino = []
    for _ in range(10):
        p = Process(target=leitura, args=(r, w, lock))
        destino.append(p)

    for p in origem + destino:
        p.start()           # Inicia execução dos processos

    for p in origem + destino:
        p.join()           # Aguarda término de execução dos processos