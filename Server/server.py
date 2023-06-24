import socket
import os
import threading
from os import sys

# Abre o arquivo e envia a imagem escolhida pelo usuário
def enviaImagem(conexaoCliente, nomeArquivo):
    with open(nomeArquivo, 'rb') as file:
        arquivoLido = file.read()
        conexaoCliente.sendall(arquivoLido)

# Envia a lista de imagens e recebe a resposta do usuário de qual imagem ele deseja
def trataCliente(conexaoCliente):
    # Enviar a lista de imagens disponíveis
    imagens = os.listdir('imagens')
    quantidadeImagens = len(imagens)
    conexaoCliente.send(str(quantidadeImagens).encode())

    nomesImagens = ''
    for image_name in imagens:
        nomesImagens += f"{image_name}\n"

    conexaoCliente.send(nomesImagens.encode())

    try:
        # Receber a escolha do cliente
        escolhaUsuario = int(conexaoCliente.recv(1024).decode())
        imagemEscolhida = os.path.join('imagens', imagens[escolhaUsuario - 1])
        conexaoCliente.sendall(imagemEscolhida.encode())
        enviaImagem(conexaoCliente, imagemEscolhida)
    except ValueError:
        # Fechar a conexão
        pass
    finally:
        conexaoCliente.close()

def iniciaServer():
    host = '127.0.0.1'
    porta = 12000

    # Criação do socket e vincula do endereço e porta
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, porta))

    # O servidor entra em modo de escuta
    serverSocket.listen(1)
    print('Servidor aguardando conexões...')

    while True:
        try:
            # Aceitar uma nova conexão
            conexaoCliente, addr = serverSocket.accept()
            print('Cliente conectado:', addr)

            # Tratar a conexão do cliente em uma nova thread
            thread =  threading.Thread(target=trataCliente, args=(conexaoCliente,))
            thread.start()
        except KeyboardInterrupt:
            # Encerrar o servidor quando o usuário pressionar Ctrl+C
            break

    # Fechar o socket do servidor
    serverSocket.close()

if __name__ == '__main__':
    iniciaServer()