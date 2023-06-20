import socket
import PySimpleGUI as sg
import os

client_socket = None  # Variável global para o socket do cliente
window = None  # Variável global para a janela

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
        mensagem = f"A imagem {nomeArquivo} foi recebida com sucesso"
        sg.popup(mensagem, title='Imagem Recebida')  # Exibir mensagem em uma janela de pop-up
        recebeImagem(clienteSocket, resposta)

    # Fecha a conexão
    clienteSocket.close()

def fecharConexao():
    global client_socket
    if client_socket:
        client_socket.close()

# Responsável por encerrar a conexão ao clicar no botão de fechar (X)
def fecharJanela():
    fecharConexao()
    window.close()

def iniciaCliente():
    global client_socket, window
    host = '127.0.0.1'
    porta = 12000

    # Criação do socket e conexão com o servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, porta))

    # Receber a lista de imagens disponíveis
    contadorImagem = int(client_socket.recv(1024).decode())

    nomeImagem = client_socket.recv(1024).decode()

    # Layout da janela
    layout = [
        [sg.Text('Escolha uma opção:')],
        [sg.Combo(nomeImagem.split("\n"), key='-ESCOLHA-', size=(20, 1))],
        [sg.Button('Enviar')]
    ]

    # Criação da janela
    window = sg.Window('Cliente', layout, size=(300, 100))

    # Loop de eventos
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            fecharJanela()
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
            enviarEscolha(client_socket, escolha)
            break

if __name__ == '__main__':
    iniciaCliente()
