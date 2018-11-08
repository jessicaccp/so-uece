"""

Cenário: comunicação de um processo com outro processo via memória compartilhada

Origem: processo que escreve
Destino: processo que lê

1 processo origem escreve e outro 1 processo destino lê, exibindo a mensagem em seguida

"""

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value
from os import getpid
from random import randint

# Lê variáveis alocadas na memória compartilhada
def leitura(num, pid, lock):
    # Fecha trava para que valores salvos na memória compartilhada não sejam alterados no meio da leitura
    lock.acquire()

    # Exibe PID do processo destino, variável numérica e PID do processo origem
    # que escreveu na variável, que também foi passado via memória compartilhada
    print("Processo %s recebeu o valor %s do processo %s"
            % (getpid(), num.value, pid.value))

    # Abre trava
    lock.release()

# Altera os valores das variáveis alocadas na memória compartilhada
def escrita(num, pid, lock):
    # Fecha trava para que outro processo não tente acessar variáveis durante sua escrita
    lock.acquire()

    # Altera o valor atual da variável "num"
    num.value = randint(100, 999)

    # Salva o PID do processo que alterou a variável
    pid.value = getpid()

    # Abre a trava
    lock.release()

# Realiza a comunicação via memória compartilhada entre dois processos
def main():
    # Cria trava
    lock = Lock()

    # Cria variáveis alocadas na memória compartilhada, ambas do tipo int e inicializadas em zero
    num = Value('i', 0)
    pid = Value('i', 0)

    # Cria processos e atribui a cada um a função que executarão
    origem = Process(target=escrita, args=(num, pid, lock))
    destino = Process(target=leitura, args=(num, pid, lock))

    # Inicia a execução dos processos e faz processo pai aguardar o término de execução dos mesmos
    origem.start()
    origem.join()

    destino.start()
    destino.join()

if __name__ == '__main__':
    main()