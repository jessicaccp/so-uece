"""

Cenário: comunicação de um processo com outro processo via memória compartilhada

Origem: processo que escreve
Destino: processo que lê

1 processo origem escreve e outro 1 processo destino lê, exibindo a mensagem em seguida

"""

from multiprocessing import Process
from multiprocessing.sharedctypes import Value
from os import getpid
from random import randint

# Lê variáveis alocadas na memória compartilhada
def leitura(num, pid):
    # Exibe PID do processo destino, valor da variável e PID do processo origem
    # que escreveu na variável, que também foi passado via memória compartilhada
    print("Processo %s recebeu o valor %s do processo %s"
            % (getpid(), num.value, pid.value))

# Altera os valores das variáveis alocadas na memória compartilhada
def escrita(num, pid):
    # Incrementa o valor atual da variável "num"
    num.value += 1

    # Salva o PID do processo que alterou a variável
    pid.value = getpid()

# Realiza a comunicação via memória compartilhada entre dois processos
def main():
    # Cria variáveis alocadas na memória compartilhada, ambas do tipo int e inicializadas em zero
    num = Value('i', 0)
    pid = Value('i', 0)

    # Cria processos e atribui a cada um a função que executarão
    origem = Process(target=escrita, args=(num, pid))
    destino = Process(target=leitura, args=(num, pid))

    # Inicia a execução dos processos e faz processo pai aguardar o término de execução dos mesmos
    origem.start()
    destino.start()

    origem.join()
    destino.join()

if __name__ == '__main__':
    main()