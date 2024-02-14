from socket import *
from threading import *
from tkinter import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "127.0.0.1"
portNumber = 10000

nome = input('Insira seu nome: ')
print(f'Olá, {nome}')

clientSocket.connect((hostIp, portNumber))
clientSocket.send(str(nome).encode("utf-8"))

# Layout
window = Tk()
window.title(nome+" "+"conectado por: "+ hostIp+ ":"+str(portNumber))
txtMessages = Text(window, width=50)
txtMessages.grid(row=0, column=0, padx=10, pady=10)
txtYourMessage = Entry(window, width=50)
txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

def limpaCaixaTexto():
    txtYourMessage.delete(0, 'end')
def sendMessage():
    clientMessage = txtYourMessage.get()
    #END é uma forma de especificar onde na caixa de texto você deseja que o texto seja inserido.
    txtMessages.insert(END, "\n" + nome +" : "+ clientMessage)
    clientSocket.send(clientMessage.encode("utf-8"))
    limpaCaixaTexto()

btnSendMessage = Button(window, text="Send", width=20, command=sendMessage)
btnSendMessage.grid(row=2, column=0, padx=10, pady=10)


def recvMessage():
    while True:
        serverMessage = clientSocket.recv(1024).decode("utf-8")
        print(serverMessage)
        txtMessages.insert(END, "\n"+serverMessage)

recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()

window.mainloop()