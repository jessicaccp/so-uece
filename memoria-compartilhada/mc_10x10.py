from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from random import randint
from os import getpid

def leitura(num, pid, lock):
    lock.acquire()
    print("Processo %s recebeu o valor %s do processo %s"
            % (getpid(), num.value, pid.value))
    lock.release()

def escrita(num, pid, lock):
    lock.acquire()

    num.value = randint(100, 999)
    pid.value = getpid()

    lock.release()

if __name__ == '__main__':
    lock = Lock()

    num = []
    pid = []

    for _ in range(10):
        num.append(Value('i', 0))
        pid.append(Value('i', 0))

    origem = []
    for x in range(10):
        p = Process(target=escrita, args=(num[x], pid[x], lock))
        origem.append(p)

    destino = []
    for x in range(10):
        p = Process(target=leitura, args=(num[x], pid[x], lock))
        destino.append(p)

    for p in origem + destino:
        p.start()

    for p in origem + destino:
        p.join()