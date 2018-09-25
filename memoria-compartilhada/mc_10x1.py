from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
import os

def leitura(num, pid, lock):
    lock.acquire()
    print("Processo %s recebeu o valor %s do processo %s"
            % (os.getpid(), num.value, pid.value))
    lock.release()

def escrita(num, pid, lock):
    lock.acquire()
    num.value += 1
    pid.value = os.getpid()
    lock.release()

if __name__ == '__main__':
    lock = Lock()

    num = Value('i', 0)
    pid = Value('i', 0)

    origem = []
    for _ in range(10):
        p = Process(target=escrita, args=(num, pid, lock))
        origem.append(p)

    destino = Process(target=leitura, args=(num, pid, lock))

    for p in origem:
        p.start()
    destino.start()

    for p in origem:
        p.join()
    destino.join()