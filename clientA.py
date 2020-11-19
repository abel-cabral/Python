# Import socket module 
from threading import Thread
from fakeSensor import FakeSensor
import random
import socket
import json
import time

# Global Variable
fakeSensorData = FakeSensor()

def getInfo(s):    
    while True:        
        # message sent to server                
        fakeSensorData.sensorType = "Sensor de umidade"
        fakeSensorData.time = 100
        fakeSensorData.metric = random.randint(100, 1000)
        fakeSensorData.unity = "KΩ"      
        json_data = json.dumps(fakeSensorData.__dict__, sort_keys=False, indent=2)             
        s.send(json_data.encode("utf-8"))
        
        # message received from server 
        data = json.loads(s.recv(1024))
        feedback = FakeSensor(data["sensorType"], data["metric"], data["time"], data["message"], data["status"], data["unity"])
        print('Received from the server :', feedback.__dict__)
                
        time.sleep(10)
    # close the connection 
    s.close() 

def Main(): 
    HOST = '127.0.0.1'    # The remote host
    PORT = 50000              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))  #Abre uma conexao com IP e porta especificados
    print ("Conectou")

    t1 = Thread(target=getInfo, args=(s,))
    t1.start()
    t1.join()
    print ("Fechou a conexao")
 
  
if __name__ == '__main__': 
    Main()