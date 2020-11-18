import socket
from threading import Thread
import random
import time
def coleta(con):

    print ("Comecou o chat")
 #   con.sendall(nome+" 1")
    print("Enviado os númeors")
    for i in range(0, 5):
        n = round(random.uniform(0.5, 10))
        b = str(n)
        print(b)
        s.send(b.encode())
        time.sleep(1)##botei o sleep porque tava mandando os números de uma vez só (concatenada)
    while 1:
        data = s.recv(1024)
        if not data: break
        print(data.decode())
    s.close()

HOST = '127.0.0.2'    # The remote host
PORT = 50000              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST, PORT))  #Abre uma conexao com IP e porta especificados
print ("Conectou")

t1 = Thread(target=coleta, args=(s,))
t1.start()
t1.join()
print ("Fechou a conexao")
