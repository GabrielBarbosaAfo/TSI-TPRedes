# Troca de Imagens com Sockets TCP/IP e PySimpleGUI
Este é um projeto que demonstra a comunicação entre um cliente e um servidor para a troca de imagens usando sockets TCP/IP em Python. 
O cliente é implementado com a biblioteca PySimpleGUI para fornecer uma interface gráfica simples para o usuário escolher a imagem a ser enviada ao servidor.

## Requisitos
Certifique-se de ter o Python instalado em sua máquina (versão 3.6 ou superior).

Você também precisará instalar a biblioteca PySimpleGUI, caso ainda não tenha instalado. Você pode instalar o PySimpleGUI usando o pip:
pip install PySimpleGUI

# Como usar
## Servidor
O servidor é responsável por receber as conexões do cliente e aguardar as solicitações para o envio de imagens.

Certifique-se de que a pasta "imagens" esteja localizada no mesmo diretório do arquivo "server.py". Essa pasta deve conter as imagens que deseja disponibilizar para o cliente.

Para iniciar o servidor, execute o seguinte comando no terminal:
python server.py
O servidor começará a escutar em "127.0.0.1:12000" por conexões de clientes.

## Cliente
O cliente é responsável por se conectar ao servidor e interagir com o usuário para escolher a imagem a ser enviada.

Certifique-se de que a pasta "imagens" esteja localizada no mesmo diretório do arquivo "client.py". Essa pasta deve conter as imagens que deseja disponibilizar para o cliente.

Para iniciar o cliente, execute o seguinte comando no terminal:
python client.py
Uma janela gráfica será aberta exibindo as opções disponíveis de imagens. Selecione uma opção no menu suspenso e clique no botão "Enviar" para enviar a imagem ao servidor.

## Conclusão
Este projeto demonstra uma implementação simples de troca de imagens usando sockets TCP/IP em Python, com uma interface gráfica básica usando PySimpleGUI. 
Ele pode servir como ponto de partida para projetos mais complexos envolvendo comunicação de rede e interações com o usuário.
