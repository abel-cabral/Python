# import socket programming library
from fakeSensor import FakeSensor
from threading import Thread
import socket

# import thread module
from _thread import *
import threading
import json

print_lock = threading.Lock()

# client and statistics
password = "CFT10"
admin = ""
connection = []
connectionNumber = 0


def activerWater(sensor, index, time):
    fakeSensorData = sensor[1] # Sensor data
    fakeSensorData.status = True
    fakeSensorData.time = time
    
    conn = sensor[0]
    json_data = json.dumps(fakeSensorData.__dict__, sort_keys=False, indent=2)        
    conn.sendall(json_data.encode("utf-8"))
    connection.pop(index)    


def engenier():
    global admin
    for i in range(len(connection)):
        fakeSensorData = connection[i][1] # Sensor data
        umidade = int(fakeSensorData.metric) # http://mundoprojetado.com.br/medindo-a-umidade-do-solo/
        # 300 - Valores abaixo de 300 indicam que o solo está seco
        # 700 - Valores acima de 700 indicam que o solo está com a umidade ideal
        
        if(umidade <= 300):
            # mensagem de alerta ao dono e molha
            activerWater(connection[i], i, 14) # client connection                             
            if (admin != ""):                
                message = "A planta X esta muito seca, abaixo de 300, verifique o vaso ou a mangueira de irrigação"                
                admin.send(message.encode("utf-8"))
        elif(umidade > 300 and umidade < 700):
            # apenas molha         
            activerWater(connection[i], i, 7) # client connection            
        else:
            # não é necessario molhar
            connection.pop(i)


def waitSensors(conn, addr, i):
    global admin
    while True:
        print ('Connected by', addr)
        data = conn.recv(1024)  # Recebe os dados
        # Check if is the admin        
        if(data.decode("utf-8") == password and admin == ""):
            admin = conn
            admin.send("Connected to server".encode("utf-8"))            
        else:            
            try:
                dataAndStatistic = []                
                data = json.loads(data.decode("utf-8"))                
                fakeSensorData = FakeSensor(data["sensorType"], data["metric"], data["time"], data["message"], data["status"], data["unity"])         
                
                dataAndStatistic.insert(0, conn)
                dataAndStatistic.insert(1, fakeSensorData)            
                connection.append(dataAndStatistic)
                print('Received from the client :', fakeSensorData.__dict__)
                if(len(connection) >= connectionNumber):
                    engenier()
            except:             
                print("Error")   
                conn.send("Data has been error".encode("utf-8")) 
                    
    conn.close()


def Main():
    i = 0
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 50000  # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))  # liga o socket com IP e porta
    while (True):
        s.listen(1)  # espera chegar pacotes na porta especificada
        conn, addr = s.accept()  # Aceita uma conex�o
        print ("Aceitou mais uma")

        t = Thread(target=waitSensors, args=(conn, addr, i))
        i = i + 1
        t.start()


if __name__ == '__main__':
    Main()
