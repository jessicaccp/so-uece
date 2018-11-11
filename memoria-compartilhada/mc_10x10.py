"""

Cenario: comunicacao de dez processos com um processo via memoria compartilhada

10 processos remetente escrevem, cada um para outro 1 processo destinatario distinto,
totalizando 10 processos destinatario, que leem e exibem as respectivas mensagens

"""

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from os import getpid
from random import randint

# Le variaveis alocadas na memoria compartilhada
def leitura(num, pid, lock):
    # Fecha trava para que valores salvos na memoria compartilhada nao sejam alterados no meio da leitura
    lock.acquire()

    # Exibe PID do processo destinatario, valor da variavel e PID do processo remetente
    # que escreveu na variavel, que tambem foi passado via memoria compartilhada
    print("Processo %s recebeu o valor %s do processo %s"
            % (getpid(), num.value, pid.value))

    # Fecha trava
    lock.release()

# Altera valores das variaveis alocadas na memoria compartilhada
def escrita(num, pid, lock):
    # Fecha trava para que outro processo nao tente acessar variaveis durante sua escrita
    lock.acquire()

    # Altera valor atual da variavel "num"
    num.value = randint(100, 999)

    # Salva o PID do processo que alterou a variavel
    pid.value = getpid()

    # Abre trava
    lock.release()

# Realiza a comunicacao via memoria compartilhada de 10 processos
# com outros 10 processos (1 para cada processo que escreve)
def main():
    # Cria trava
    lock = Lock()

    # Cria variaveis alocadas na memoria compartilhada, ambas do tipo int e inicializadas em zero
    num = []
    pid = []

    for _ in range(10):
        num.append(Value('i', 0))
        pid.append(Value('i', 0))

    # Cria processos e atribui a cada um a funcao que executarao
    remetente = []
    for x in range(10):
        p = Process(target=escrita, args=(num[x], pid[x], lock))
        remetente.append(p)

    destinatario = []
    for x in range(10):
        p = Process(target=leitura, args=(num[x], pid[x], lock))
        destinatario.append(p)

    # Inicia a execucao dos processos e faz processo pai aguardar o termino de execucao dos mesmos
    for p in remetente:
        p.start()
        p.join()

    for p in destinatario:
        p.start()
        p.join()

if __name__ == '__main__':
    main()