from multiprocessing import Process
from multiprocessing.sharedctypes import Value, Array
import os

def leitura(num, pid):
    print("Processo %s recebeu o valor %s do processo %s"
            % (os.getpid(), num.value, pid.value))

def escrita(num, pid):
    num.value += 1
    pid.value = os.getpid()

if __name__ == '__main__':
    num = Value('i', 0)
    pid = Value('i', 0)

    origem = Process(target=escrita, args=(num, pid))
    destino = Process(target=leitura, args=(num, pid))

    origem.start()
    destino.start()

    origem.join()
    destino.join()