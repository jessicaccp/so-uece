"""

Cenario: comunicacao de dez processos com dez processos via pipe

10 processos remetente escrevem, cada um para outro 1 processo destinatario distinto,
totalizando 10 processos destinatario, que leem e exibem as respectivas mensagens

"""

from multiprocessing import Pipe, Process, Lock
from os import getpid

# Recebe dados do processo remetente via pipe
def leitura(r, w, lock):
    # Fecha a escrita no pipe
    w.close()
    
    # Fecha trava para que a mensagem nao seja alterada antes do print
    lock.acquire()

    # Recebe mensagem e a exibe no terminal junto com seu PID
    mensagem = r.recv()
    print("Processo %s recebeu: %s" % (getpid(), mensagem))

    # Abre trava
    lock.release()

    # Fecha a leitura do pipe
    r.close()

# Envia dados para o processo destinatario via pipe
def escrita(r, w, lock):
    # Fecha a leitura do pipe
    r.close()

    # Fecha trava para que a mensagem nao seja alterada antes de ser enviada
    lock.acquire()

    # Define mensagem contendo seu PID e a envia
    mensagem = "\"Saudacoes do processo %s!\"" % getpid()
    w.send(mensagem)

    # Abre trava
    lock.release()

    # Fecha a escrita no pipe
    w.close()

# Realiza a comunicacao via pipe de 10 processos com outros 10 processos (1 para cada processo que escreve)
def main():
    # Cria o pipe e a trava usada para exclusao mutua na regiao critica
    r, w = Pipe()
    lock = Lock()

    # Cria processos e atribui a cada um a funcao que executarao
    remetente = []
    for _ in range(10):
        p = Process(target=escrita, args=(r, w, lock))
        remetente.append(p)
    
    destinatario = []
    for _ in range(10):
        p = Process(target=leitura, args=(r, w, lock))
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