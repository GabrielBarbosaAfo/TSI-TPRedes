import socket
import PySimpleGUI as sg
import os
from _tkinter import TclError

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
    clienteSocket.sendall(str(escolhaCliente).encode("utf-8"))

    while True:
        try:
            resposta = clienteSocket.recv(1024).decode("utf-8")
            if not resposta:
                break
            _, arquivo = os.path.split(resposta)
            nomeArquivo = os.path.splitext(arquivo)[0]  # Utilizado para separar o nome do arquivo da sua extensão 
            if nomeArquivo == "Escolha inválida":
                sg.popup('Escolha inválida', title='Erro')
                break
            mensagem = f"A imagem {nomeArquivo} foi recebida com sucesso"
            sg.popup(mensagem, title='Imagem Recebida')  # Exibir mensagem em uma janela de pop-up
            recebeImagem(clienteSocket, resposta)
        except ConnectionResetError:
            # Encerrar a conexão se ocorrer um erro de conexão
            break

    # Fecha a conexão
    clienteSocket.close()

def fecharConexao():
    if client_socket:
        client_socket.close()

def fecharJanela():
    fecharConexao()
    if window != None:
        window.close()

def iniciaCliente():
    global client_socket, window
    host = '127.0.0.1'
    porta = 12000

    try:
        # Criação do socket e conexão com o servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, porta))
    
    
        # Receber a lista de imagens disponíveis
        contadorImagem = int(client_socket.recv(1024).decode("utf-8"))

        nomeImagem = client_socket.recv(1024).decode("utf-8")

        # Layout da janela
        layout = [
            [sg.Text('Escolha uma opção:')],
            [sg.Combo(nomeImagem.split("\r"), key='-ESCOLHA-', readonly=True, size=(20, 1))],
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
                for nome in nomeImagem.split("\r"):
                    if escolha == nome:
                        escolha = i
                        break
                    else:
                        i += 1

                if 0 <= escolha - 1 < len(nomeImagem.split("\r")):
                    enviarEscolha(client_socket, escolha)
                    break
                else:
                    sg.popup('Escolha inválida', title='Erro')
                    continue
    except KeyboardInterrupt:
        sg.popup('Ocorreu um erro', title='Erro')
    except ConnectionRefusedError:
        sg.popup('Não foi possível conectar ao servidor. Certifique-se de que o servidor esteja em execução.', title='Erro de Conexão')
    except TclError:
        print("Não há um display disponível para a interface gráfica do PySimpleGUI!!!")
    finally:
        fecharJanela()

if __name__ == '__main__':
    try:
        iniciaCliente()
    except ConnectionResetError:
        fecharConexao()
