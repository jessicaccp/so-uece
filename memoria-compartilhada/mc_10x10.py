"""

Cenário: comunicação de dez processos com um processo via memória compartilhada

Origem: processo que escreve
Destino: processo que lê

10 processos origem escrevem, cada um para outro 1 processo destino distinto,
totalizando 10 processos destino, que leem e exibem as respectivas mensagens

"""

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from os import getpid
from random import randint

# Lê variáveis alocadas na memória compartilhada
def leitura(num, pid, lock):
    # Fecha trava para que valores salvos na memória compartilhada não sejam alterados no meio da leitura
    lock.acquire()

    # Exibe PID do processo destino, valor da variável e PID do processo origem
    # que escreveu na variável, que também foi passado via memória compartilhada
    print("Processo %s recebeu o valor %s do processo %s"
            % (getpid(), num.value, pid.value))

    # Fecha trava
    lock.release()

# Altera valores das variáveis alocadas na memória compartilhada
def escrita(num, pid, lock):
    # Fecha trava para que outro processo não tente acessar variáveis durante sua escrita
    lock.acquire()

    # Altera valor atual da variável "num"
    num.value = randint(100, 999)

    # Salva o PID do processo que alterou a variável
    pid.value = getpid()

    # Abre trava
    lock.release()

# Realiza a comunicação via memória compartilhada de 10 processos
# com outros 10 processos (1 para cada processo que escreve)
def main():
    # Cria trava
    lock = Lock()

    # Cria variáveis alocadas na memória compartilhada, ambas do tipo int e inicializadas em zero
    num = []
    pid = []

    for _ in range(10):
        num.append(Value('i', 0))
        pid.append(Value('i', 0))

    # Cria processos e atribui a cada um a função que executarão
    origem = []
    for x in range(10):
        p = Process(target=escrita, args=(num[x], pid[x], lock))
        origem.append(p)

    destino = []
    for x in range(10):
        p = Process(target=leitura, args=(num[x], pid[x], lock))
        destino.append(p)

    # Inicia a execução dos processos e faz processo pai aguardar o término de execução dos mesmos
    for p in origem:
        p.start()
        p.join()

    for p in destino:
        p.start()
        p.join()

if __name__ == '__main__':
    main()