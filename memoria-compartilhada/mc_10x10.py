"""

Cenário: comunicação de dez processos com um processo via memória compartilhada

Origem: processo que escreve
Destino: processo que lê

10 processos origem escrevem, cada um para outro 1 processo destino distinto,
totalizando 10 processos destino, que leem e exibem as respectivas mensagens

"""

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from random import randint
from os import getpid

# Lê variáveis alocadas na memória compartilhada
def leitura(num, pid, lock):
    # Fecha trava para que valores salvos na memória compartilhada não sejam alterados no meio da leitura
    lock.acquire()
    # Exibe PID do processo destino, valor da variável e PID do processo origem
    # que escreveu na variável, que também foi passado via memória compartilhada
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

    for p in origem:
        p.start()
        p.join()

    for p in destino:
        p.start()
        p.join()