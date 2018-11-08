"""

Cenário: comunicação de dez processos com dez processos via pipe

Origem: processo que escreve
Destino: processo que lê

10 processos origem escrevem, cada um para outro 1 processo destino distinto,
totalizando 10 processos destino, que leem e exibem as respectivas mensagens

"""

from multiprocessing import Pipe, Process, Lock
from os import getpid

# Recebe dados do processo origem via pipe
def leitura(r, w, lock):
    # Fecha a escrita no pipe
    w.close()
    
    # Fecha trava para que a mensagem não seja alterada antes do print
    lock.acquire()

    # Recebe mensagem e a exibe no terminal junto com seu PID
    mensagem = r.recv()
    print("Processo %s recebeu: %s" % (getpid(), mensagem))

    # Abre trava
    lock.release()

    # Fecha a leitura do pipe
    r.close()

# Envia dados para o processo destino via pipe
def escrita(r, w, lock):
    # Fecha a leitura do pipe
    r.close()

    # Fecha trava para que a mensagem não seja alterada antes de ser enviada
    lock.acquire()

    # Define mensagem contendo seu PID e a envia
    mensagem = "\"Saudações do processo %s!\"" % getpid()
    w.send(mensagem)

    # Abre trava
    lock.release()

    # Fecha a escrita no pipe
    w.close()

# Realiza a comunicação via pipe de 10 processos com outros 10 processos (1 para cada processo que escreve)
def main():
    # Cria o pipe e a trava usada para exclusão mútua na região crítica
    r, w = Pipe()
    lock = Lock()

    # Cria processos e atribui a cada um a função que executarão
    origem = []
    for _ in range(10):
        p = Process(target=escrita, args=(r, w, lock))
        origem.append(p)
    
    destino = []
    for _ in range(10):
        p = Process(target=leitura, args=(r, w, lock))
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