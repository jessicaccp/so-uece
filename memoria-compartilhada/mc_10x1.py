from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
import os

def leitura(msg, lock):
    lock.acquire()
    for x in range(0, 20, 2):
        print("Processo %s recebeu o valor %s do processo %s"
                % (os.getpid(), msg[x], msg[x + 1]))
    lock.release()

def escrita(num, pid, msg, lock):
    lock.acquire()

    num.value += 1
    pid.value = os.getpid()

    x = (num.value - 1) * 2
    msg[x] = num.value
    msg[x + 1] = pid.value

    lock.release()

if __name__ == '__main__':
    lock = Lock()

    num = Value('i', 0)
    pid = Value('i', 0)
    msg = Array('i', range(20))

    origem = []
    for _ in range(10):
        p = Process(target=escrita, args=(num, pid, msg, lock))
        origem.append(p)

    destino = Process(target=leitura, args=(msg, lock))

    for p in origem:
        p.start()

    for p in origem:
        p.join()

    destino.start()
    destino.join()