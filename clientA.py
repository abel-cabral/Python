# Import socket module 
from fakeSensor import FakeSensor
import random
import socket
import json
import time

# Global Variable
fakeSensorData = FakeSensor()

def Main(): 
    # local host IP '127.0.0.1' 
    host = '127.0.0.1'
  
    # Define the port on which you want to connect 
    port = 12345
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server on local computer 
    s.connect((host, port)) 
      
    while True:
        # message sent to server                
        fakeSensorData.sensorType = "Sensor de umidade"
        fakeSensorData.time = 100
        fakeSensorData.metric = random.randint(100, 1000)
        fakeSensorData.unity = "KΩ"      
        json_data = json.dumps(fakeSensorData.__dict__, sort_keys=False, indent=2)        
        s.sendall(json_data.encode())
        
        # message received from server 
        data = json.loads(s.recv(1024))
        feedback = FakeSensor(data["sensorType"], data["metric"], data["time"], data["message"], data["status"], data["unity"])
        print('Received from the server :', feedback.__dict__)
                
        time.sleep(10)
    # close the connection 
    s.close() 
 
  
if __name__ == '__main__': 
    Main()