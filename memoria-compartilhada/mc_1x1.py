"""

Cenario: comunicacao de um processo com outro processo via memoria compartilhada

1 processo remetente escreve e outro 1 processo destinatario le, exibindo a mensagem em seguida

"""

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value
from os import getpid
from random import randint
from time import time

# Le variaveis alocadas na memoria compartilhada
def leitura(num, pid, lock):
    # Fecha trava para que valores salvos na memoria compartilhada nao sejam alterados no meio da leitura
    lock.acquire()

    # Exibe PID do processo destinatario, variavel numerica e PID do processo remetente
    # que escreveu na variavel, que tambem foi passado via memoria compartilhada
    t = time()
    valor = num.value
    remetente = pid.value
    print("Tempo de recebimento: %s" % (time() - t))
    print("Processo %s recebeu o valor %s do processo %s"
            % (getpid(), valor, remetente))

    # Abre trava
    lock.release()

# Altera os valores das variaveis alocadas na memoria compartilhada
def escrita(num, pid, lock):
    # Fecha trava para que outro processo nao tente acessar variaveis durante sua escrita
    lock.acquire()

    t = time()
    # Altera o valor atual da variavel "num"
    num.value = randint(100, 999)

    # Salva o PID do processo que alterou a variavel
    pid.value = getpid()
    print("Tempo de envio: %s" % (time() - t))

    # Abre a trava
    lock.release()

# Realiza a comunicacao via memoria compartilhada entre dois processos
def main():
    # Cria trava
    lock = Lock()

    # Cria variaveis alocadas na memoria compartilhada, ambas do tipo int e inicializadas em zero
    num = Value('i', 0)
    pid = Value('i', 0)

    # Cria processos e atribui a cada um a funcao que executarao
    remetente = Process(target=escrita, args=(num, pid, lock))
    destinatario = Process(target=leitura, args=(num, pid, lock))

    # Inicia a execucao dos processos e faz processo pai aguardar o termino de execucao dos mesmos
    remetente.start()
    remetente.join()

    destinatario.start()
    destinatario.join()

if __name__ == '__main__':
    main()