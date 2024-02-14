from socket import *
from threading import *
import datetime

clients = set()
nomes_clientes = {}
  

def clientThread(clientSocket):
    nome_cliente = nomes_clientes[clientSocket]
    
    while True:
        # data e data formatada
        date = datetime.datetime.now()
        date = date.strftime('%d/%m/%Y %H:%M:%S')

        try:
            message = clientSocket.recv(1024).decode("utf-8")# recebe msg do cliente
            print(nome_cliente + ": "+ message)
            for client in clients: ## envia msg em Brodcasting
                if client is not clientSocket:
                    client.send(str(date+'\n'+nome_cliente +": "+ message).encode("utf-8"))

        except ConnectionResetError: #caso algun cliente saia do chat
            for client in clients:
                    if client is not clientSocket:
                        client.send(str(date+'\n'+nome_cliente +" saiu do chat ").encode("utf-8"))
            ## remove cliente
            print(f'cliente  {nome_cliente} saiu')
            clients.remove(clientSocket)
            del nomes_clientes[clientSocket]
            clientSocket.close() ## enecerra a coneção do cliente
            break
    

hostSocket = socket(AF_INET, SOCK_STREAM) # Cria um socket tcp/ip
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1) #permitindo que o endereço do soquete seja reutilizado imediatamente após o encerramento do soquete anterior

hostIp = "0.0.0.0"
portNumber = 10000
hostSocket.bind((hostIp, portNumber)) # Associa Ip:porta ao um socket
hostSocket.listen() # Aguarda conexção
print ("Aguardando conexção...")


while True:
    clientSocket, clientAddress = hostSocket.accept() ## Obtém a conexção
    nome_cliente = clientSocket.recv(1024).decode('utf-8')
    clients.add(clientSocket)
    nomes_clientes[clientSocket] = nome_cliente

    date = datetime.datetime.now()
    date = date.strftime('%d/%m/%Y %H:%M:%S')
    for client in clients: ## envia msg de entrada em brodcasting 
        client.send(str(date+'\n'+nome_cliente +" Entrou no chat ").encode("utf-8"))
    print ("Conectado por: " + nome_cliente)

    thread = Thread(target=clientThread, args=(clientSocket,))
    thread.start()
    