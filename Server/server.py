import socket
import os

#Abre o arquivo e evia a imagem escolhida pelo usuario
def enviaImagem(conexaoCliente, nomeArquivo):
    with open(nomeArquivo, 'rb') as file:
        arquivoLido = file.read()
        conexaoCliente.sendall(arquivoLido)

#Envia a lista de imagens e recebe a resposta do usuario de qual imagem ele deseja
def trataCliente(conexaoCliente):

    # Enviar a lista de imagens disponíveis
    imagens = os.listdir('imagens')
    quantidadeImagens = len(imagens)
    conexaoCliente.send(str(quantidadeImagens).encode())

    numeroImg = 1 
    nomesImagens = '' 
    for image_name in imagens:
        nomesImagens += f"{numeroImg} - {image_name}\n"  
        numeroImg += 1

    conexaoCliente.send(nomesImagens.encode())

    # Receber a escolha do cliente
    escolhaUsuario = int(conexaoCliente.recv(1024).decode())

    if escolhaUsuario < 1 or escolhaUsuario > quantidadeImagens:
        conexaoCliente.sendall('Escolha inválida!'.encode())
    else:
        imagemEscolhida = os.path.join('imagens', imagens[escolhaUsuario - 1])
        conexaoCliente.sendall(imagemEscolhida.encode())
        enviaImagem(conexaoCliente, imagemEscolhida)

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
        # Aceitar uma nova conexão
        conexaoCliente, addr = serverSocket.accept()
        print('Cliente conectado:', addr)

        # Tratar a conexão do cliente
        trataCliente(conexaoCliente)

        # Fechar a conexão
        conexaoCliente.close()
        print('Conexão encerrada com:', addr)

if __name__ == '__main__':
    iniciaServer()
