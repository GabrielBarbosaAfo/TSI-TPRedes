import socket
import PySimpleGUI as sg
import os

# Recebe a imagem colocando-a na pasta imagens
def recebeImagem(clienteSocket, nomeArquivo):
    with open(nomeArquivo, 'wb') as file:
        while True:
            imagem = clienteSocket.recv(1024)
            if not imagem:
                break
            file.write(imagem)

# Função para lidar com o clique do botão Enviar
def enviarEscolha(clienteSocket, escolha):
    escolhaCliente = int(escolha)

    # Enviar a escolha para o servidor
    clienteSocket.sendall(str(escolhaCliente).encode())

    while True:
        resposta = clienteSocket.recv(1024).decode()
        if not resposta:
            break
        _, arquivo = os.path.split(resposta)
        nomeArquivo = os.path.splitext(arquivo)[0]
        print(f"A imagem {nomeArquivo} foi recebida com sucesso")
        recebeImagem(clienteSocket, resposta)

    # Fecha a conexão
    clienteSocket.close()

def iniciaCliente():
    host = '127.0.0.1'
    porta = 12000

    # Criação do socket e conexão com o servidor
    clienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clienteSocket.connect((host, porta))

    # Receber a lista de imagens disponíveis
    contadorImagem = int(clienteSocket.recv(1024).decode())

    nomeImagem = clienteSocket.recv(1024).decode()

    print(f"Imagens disponíveis:\n{nomeImagem}\n")

    # Layout da janela
    layout = [
        [sg.Text('Escolha uma opção:')],
        [sg.Combo(nomeImagem.split("\n"), key='-ESCOLHA-', size = (20,1))],
        [sg.Button('Enviar')]
    ]

    # Criação da janela
    window = sg.Window('Cliente', layout)

    # Loop de eventos
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Enviar':
            escolha = values['-ESCOLHA-']
            i = 1
            for nome in nomeImagem.split("\n"):
                if escolha == nome:
                    escolha = i
                    break
                else:
                    i += 1
            enviarEscolha(clienteSocket, escolha)
            break

    # Fechamento da janela
    window.close()

if __name__ == '__main__':
    iniciaCliente()
