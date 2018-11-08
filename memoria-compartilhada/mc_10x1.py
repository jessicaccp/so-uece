"""

Cenário: comunicação de dez processos com um processo via memória compartilhada

Origem: processo que escreve
Destino: processo que lê

10 processos origem escrevem e outro 1 processo destino lê, exibindo as mensagens em seguida

"""

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from os import getpid
from random import randint

# Lê variáveis alocadas na memória compartilhada
def leitura(msg, lock):
    # Fecha trava para que valores salvos na memória compartilhada não sejam alterados no meio da leitura
    lock.acquire()

    # Faz a leitura para cada um dos 10 processos de origem. No caso, o Array "msg"
    # contém 20 valores, onde, dois a dois, foram escritos pelos 10 processos.
    # O primeiro dos valores é um número aleatório de 3 dígitos e o segundo o PID do processo
    for x in range(0, 20, 2):
        # Exibe PID do processo destino, valor aleatório gerado pelo processo origem
        # e PID do processo origem que fez a escrita
        print("Processo %s recebeu o valor %s do processo %s"
                % (getpid(), msg[x], msg[x + 1]))

    # Abre trava
    lock.release()

# Altera valores das variáveis alocadas na memória compartilhada
def escrita(num, pid, msg, lock, index):
    # Fecha trava para que outro processo não tente acessar variáveis durante sua escrita
    lock.acquire()

    # Altera valor atual da variável "num"
    num.value = randint(100, 999)

    # Salva PID do processo que alterou a variável
    pid.value = getpid()

    # Calcula em que espaço do Array deve salvar os dois valores que acabou de alterar.
    # O processo destino, que fará a leitura, lerá exatamente esse Array "msg", portanto,
    # o processo 1 salva nos espaços 0 e 1, o processo 2 em 2 e 3 e assim sucessivamente.
    index.value += 1
    x = (index.value - 1) * 2

    # Escreve os valores no Array
    msg[x] = num.value
    msg[x + 1] = pid.value

    # Abre a trava
    lock.release()

# Realiza a comunicação via memória compartilhada de 10 processos com outro processo
def main():
    # Cria trava
    lock = Lock()

    # Cria variáveis alocadas na memória compartilhada, sendo duas do tipo int
    # e inicializadas em zero e outra um Array do tipo int de tamanho 20
    num = Value('i', 0)
    pid = Value('i', 0)
    msg = Array('i', range(20))

    # Cria variável que auxilia na escrita dos valores de "num" e "pid"
    # no Array, compartilhada entre os processos origem
    index = Value('i', 0)

    # Cria processos e atribui a cada um a função que executarão
    origem = []
    for _ in range(10):
        p = Process(target=escrita, args=(num, pid, msg, lock, index))
        origem.append(p)

    destino = Process(target=leitura, args=(msg, lock))

    # Inicia a execução dos processos e faz processo pai aguardar o término de execução dos mesmos
    for p in origem:
        p.start()
        p.join()

    destino.start()
    destino.join()

if __name__ == '__main__':
    main()