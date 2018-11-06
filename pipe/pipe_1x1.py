"""

Cenário: comunicação de um processo com outro processo via pipe

Origem: processo que escreve
Destino: processo que lê

1 processo origem escreve para outro 1 processo destino, que lê e exibe mensagem

"""

from multiprocessing import Pipe, Process
import os

# Recebe dados do processo origem
def leitura(r, w):
    # Fecha a escrita no pipe
    w.close()

    # Recebe mensagem e a exibe no terminal junto com seu PID
    mensagem = r.recv()
    print("Processo %s recebeu: %s" % (os.getpid(), mensagem))

    # Fecha a leitura do pipe
    r.close()

# Envia dados para o processo destino
def escrita(r, w):
    # Fecha a leitura do pipe
    r.close()

    # Define mensagem contendo seu PID e a envia
    mensagem = "\"Saudações do processo %s!\"" % os.getpid()
    w.send(mensagem)

    # Fecha a escrita no pipe
    w.close()

# Realiza a comunicação via pipe entre os dois processos
def main():
    # Cria pipe
    r, w = Pipe()

    # Cria processos e atribui a cada um a função que executarão
    origem = Process(target=escrita, args=(r, w))
    destino = Process(target=leitura, args=(r, w))

    # Inicia a execução dos processos e faz processo pai aguardar o término de execução dos mesmos
    origem.start()
    origem.join()

    destino.start()
    destino.join()

if __name__ == '__main__':
    main()