import socket
import os
import threading

# Open the file and send the chosen image to the client
def enviaImagem(conexaoCliente, nomeArquivo):
    with open(nomeArquivo, 'rb') as file:
        arquivoLido = file.read()
        conexaoCliente.sendall(arquivoLido)

# Send the list of images and receive the user's choice
def trataCliente(conexaoCliente):
    imagens = os.listdir('imagens')
    quantidadeImagens = len(imagens)
    conexaoCliente.send(str(quantidadeImagens).encode("utf-8"))

    nomesImagens = ''
    for image_name in imagens:
        nomesImagens += f"{image_name}\r"

    conexaoCliente.send(nomesImagens.encode("utf-8"))

    try:
        escolhaUsuario = int(conexaoCliente.recv(1024).decode("utf-8"))
        imagemEscolhida = os.path.join('imagens', imagens[escolhaUsuario - 1])
        conexaoCliente.sendall(imagemEscolhida.encode("utf-8"))
        enviaImagem(conexaoCliente, imagemEscolhida)
    except (ValueError, KeyboardInterrupt):
        pass
    finally:
        conexaoCliente.close()

def iniciaServer():
    host = '127.0.0.1'
    porta = 12000

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, porta))

    serverSocket.listen(1)
    print('Servidor aguardando conexões...')

    # Lista para armazenar as threads ativas
    thread_list = []

    while True:
        try:
            conexaoCliente, addr = serverSocket.accept()
            print('Cliente conectado:', addr)

            thread = threading.Thread(target=trataCliente, args=(conexaoCliente,))
            thread_list.append(thread)
            thread.daemon = True
            thread.start()
        except KeyboardInterrupt:
            print("\nConexão Interrompida")
            fecharThreads(thread_list)
            break

    serverSocket.close()

def fecharThreads(thread_list):
    for thread in thread_list:
        thread.join(0)

if __name__ == '__main__':
    iniciaServer()
