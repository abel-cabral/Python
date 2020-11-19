# import socket programming library
from fakeSensor import FakeSensor
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
    conn.sendall(json_data.encode())
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
                admin.send(message.encode())
        elif(umidade > 300 and umidade < 700):
            # apenas molha         
            activerWater(connection[i], i, 7) # client connection            
        else:
            # não é necessario molhar
            connection.pop(i)


def waitSensors(conn):
    global admin
    while True:
        try:
            dataAndStatistic = []                      
            data = json.loads(conn.recv(1024))
            fakeSensorData = FakeSensor(data["sensorType"], data["metric"], data["time"], data["message"], data["status"], data["unity"])                        
            
            dataAndStatistic.insert(0, conn)
            dataAndStatistic.insert(1, fakeSensorData)            
            connection.append(dataAndStatistic)
            print('Received from the server :', fakeSensorData.__dict__)
            if(len(connection) >= connectionNumber):
                engenier()
        except:
            # Check if is the admin            
            if(conn.recv(1024) == password):
                admin = conn
                print("Admin ON")
            else:
                conn.send("Data has been error".encode()) 
    conn.close()


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        conn, addr = s.accept()               
        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        start_new_thread(waitSensors, (conn,))
    s.close()


if __name__ == '__main__':
    Main()
