"""

Cenario: comunicacao de dez processos com um processo via memoria compartilhada
10 processos remetente escrevem e outro 1 processo destinatario le, exibindo as mensagens em seguida

"""

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from os import getpid
from random import randint
from time import time
import psutil

# Lê variaveis alocadas na memoria compartilhada
def leitura(msg, lock):
    # Fecha trava para que valores salvos na memoria compartilhada nao sejam alterados no meio da leitura
    lock.acquire()

    # Faz a leitura para cada um dos 10 processos de remetente. No caso, o Array "msg"
    # contem 20 valores, onde, dois a dois, foram escritos pelos 10 processos.
    # O primeiro dos valores e um numero aleatorio de 3 digitos e o segundo o PID do processo
    for x in range(0, 20, 2):
        # Exibe PID do processo destinatario, valor aleatorio gerado pelo processo remetente
        # e PID do processo remetente que fez a escrita e calcula tempo de comunicacao
        t = time()
        valor = msg[x]
        remetente = msg[x + 1]
        print("Tempo de recebimento: %s" % (time() - t))
        print("Processo %s recebeu o valor %s do processo %s"
                % (getpid(), valor, remetente))

    # Abre trava
    lock.release()

    # Calcula uso de memoria do processo
    p = psutil.Process(getpid())
    print("Destinatario:", p.memory_info())

# Altera valores das variaveis alocadas na memoria compartilhada
def escrita(num, pid, msg, lock, index):
    # Fecha trava para que outro processo nao tente acessar variaveis durante sua escrita
    lock.acquire()

    # Altera valor atual da variavel "num"
    num.value = randint(100, 999)

    # Salva PID do processo que alterou a variavel
    pid.value = getpid()

    # Calcula em que espaco do Array deve salvar os dois valores que acabou de alterar.
    # O processo destinatario, que fara a leitura, lera exatamente esse Array "msg", portanto,
    # o processo 1 salva nos espacos 0 e 1, o processo 2 em 2 e 3 e assim sucessivamente.
    index.value += 1
    x = (index.value - 1) * 2

    # Escreve os valores no Array e calcula tempo de comunicacao
    t = time()
    msg[x] = num.value
    msg[x + 1] = pid.value
    print("Tempo de envio: %s" % (time() - t))

    # Abre a trava
    lock.release()

    # Calcula uso de memoria do processo
    p = psutil.Process(getpid())
    print("Remetente:", p.memory_info())

# Realiza a comunicacao via memoria compartilhada de 10 processos com outro processo
def main():
    # Cria trava
    lock = Lock()

    # Cria variaveis alocadas na memoria compartilhada, sendo duas do tipo int
    # e inicializadas em zero e outra um Array do tipo int de tamanho 20
    num = Value('i', 0)
    pid = Value('i', 0)
    msg = Array('i', range(20))

    # Cria variavel que auxilia na escrita dos valores de "num" e "pid"
    # no Array, compartilhada entre os processos remetente
    index = Value('i', 0)

    # Cria processos e atribui a cada um a funcao que executarao
    remetente = []
    for _ in range(10):
        p = Process(target=escrita, args=(num, pid, msg, lock, index))
        remetente.append(p)

    destinatario = Process(target=leitura, args=(msg, lock))

    # Inicia a execucao dos processos e faz processo pai aguardar o termino de execucao dos mesmos
    for p in remetente:
        p.start()
        p.join()

    destinatario.start()
    destinatario.join()

if __name__ == '__main__':
    main()