import socket

#Recebe a imagem colocando-a na pasta imagens
def recebeImagem(clienteSocket, nomeArquivo):
    with open(nomeArquivo, 'wb') as file:
        while True:
            imagem = clienteSocket.recv(1024)
            if not imagem:
                break
            file.write(imagem)

#Recebe a lista de imagens e retorna o a escolhida pelo cliente
def iniciaCliente():
    host = '127.0.0.1'
    porta = 12000

    # Criação do socket e conexão com o servidor
    clienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clienteSocket.connect((host, porta))

    # Receber a lista de imagens disponíveis
    contadorImagem = int(clienteSocket.recv(1024).decode())

    nomeImagem = clienteSocket.recv(1024).decode()
    print(f"Imagens disponiveis:\n{nomeImagem}\n")

    while True:
        escolhaCliente = int(input('Digite sua escolha: '))

        # Enviar a escolha para o servidor
        clienteSocket.sendall(str(escolhaCliente).encode())

        while True:
            resposta = clienteSocket.recv(1024).decode()
            if not resposta:
                break
            formatandoImagem = resposta.split('/')[1]
            imagemFormatada = formatandoImagem.split('.')[0]
            print(f"A imagem {imagemFormatada} foi recebida com sucesso")
            recebeImagem(clienteSocket, resposta)
        break

    # Fecha a conexão
    clienteSocket.close()

if __name__ == '__main__':
    iniciaCliente()