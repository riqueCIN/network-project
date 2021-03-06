from socket import socket, AF_INET, SOCK_STREAM
from _thread import *

host = 'localhost'
porta = 80
modelo = "modelo.html"

def servidor(socket_client):
    while True:
        data = socket_client.recv(2048)
        if not data:
            break
        data_decodif = data.decode()
        lista_requisicao = data_decodif.split(' ')
        print(lista_requisicao)
        if len(lista_requisicao) < 3 or lista_requisicao[0] != 'GET':
            header = 'HTTP/1.1 400 Bad Request\n\n'
            arquivo_lido = '<html><body><center><h3>Error 400: Bad Request</h3><p>Mensagem de requisicao nao entendida pelo servidor</p></center></body></html>'
            arquivo_lido = arquivo_lido.encode('utf-8')
            resposta_final = header.encode('utf-8')
            resposta_final += arquivo_lido
            socket_client.send(resposta_final)
            break
        if lista_requisicao[2] != 'HTTP/1.1\r\nHost:':
            header = 'HTTP/1.1 505 HTTP Version Not Supported\n\n'
            arquivo_lido = '<html><body><center><h3>Error 505: HTTP Version Not Supported</h3><p>Versao do HTTP utilizada não é suportada neste servidor</p></center></body></html>'
            arquivo_lido = arquivo_lido.encode('utf-8')
            resposta_final = header.encode('utf-8')
            resposta_final += arquivo_lido
            socket_client.send(resposta_final)
            break
        metodo = lista_requisicao[0]
        requisicao = lista_requisicao[1]
        print('Requisição do cliente:', requisicao, metodo)
        meu_arquivo = requisicao.lstrip('/')
        if meu_arquivo == '':
            meu_arquivo = 'modelo.html'
        try:
            arquivo = open(meu_arquivo,'rb')
            arquivo_lido = arquivo.read()
            arquivo.close()
            if meu_arquivo.endswith('.html'):
                mimetype = 'text/html'
            elif meu_arquivo.endswith('.htm'):
                mimetype = 'text/htm'
            elif meu_arquivo.endswith('.txt'):
                mimetype = 'text/txt'
            elif meu_arquivo.endswith('.css'):
                mimetype = 'text/css'
            elif meu_arquivo.endswith('.js'):
                mimetype = 'aplication/js'
            elif meu_arquivo.endswith('.pdf'):
                mimetype = 'application/pdf'
            elif meu_arquivo.endswith('.docx'):
                mimetype = 'application/docx'
            elif meu_arquivo.endswith('.png'):
                mimetype = 'image/png'
            elif meu_arquivo.endswith('.gif'):
                mimetype = 'image/gif'
            else:
                mimetype = 'image/jpg'
            header = 'HTTP/1.1 200 OK\n'
            header += 'Content-Type: ' + str(mimetype) + '\n\n'
        except:
            header = 'HTTP/1.1 404 Not Found\n\n'
            arquivo_lido = '<html><body><center><h3>Error 404: File not found</h3><p>Documento requisitado nao foi localizado no servidor</p></center></body></html>'
            arquivo_lido = arquivo_lido.encode('utf-8')
        resposta_final = header.encode('utf-8')
        resposta_final += arquivo_lido
        socket_client.send(resposta_final)
        break

def main():
    socket_server = socket(AF_INET, SOCK_STREAM)
    socket_server.bind((host, porta))
    socket_server.listen(3)
    while True:
        socket_client, endereco_cliente = socket_server.accept()
        start_new_thread(servidor,(socket_client,))
        print(f'Conectado com: {endereco_cliente[0]}:{endereco_cliente[1]}')

if __name__ == "__main__":
    main()