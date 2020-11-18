from threading import Thread
import socket
import time


def aceita(conn, addr,i):
    global conexoes
    global lista
    global ad
    conexoes.append(conn)
    print ('Connected by', addr)
    while 1:
        data = conn.recv(1024)  # Recebe os dados
        print (i, "enviou ", data)
        lista[i].append(float(data))
        if not data: break
        if len(lista) == 2:
            if len(lista[i]) == 5:
                for a in range(len(lista[i])):
                    ad = []
                    for c in range(len(lista)):
                        ad.append(lista[c][a])
                    enviarClient(conexoes[i],ad)


def enviarClient(j,listlocal):
    time.sleep(1)
    print(listlocal)
    aux = str(calmed(listlocal))
    j.sendall(aux.encode())  # Envia string modificada
    return []


def calmed(lista):
    media=0
    for i in lista:
        media+=i
    media=media/len(lista)
    return media


lista=[[],[]]
conexoes = []
ad = []
i = 0
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 50000  # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))  # liga o socket com IP e porta
while (1):
    s.listen(1)  # espera chegar pacotes na porta especificada
    conn, addr = s.accept()  # Aceita uma conex�o
    print ("Aceitou mais uma")

    t = Thread(target=aceita, args=(conn, addr,i))
    i = i+1
    t.start()


