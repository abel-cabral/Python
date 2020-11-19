# Import socket module 
from fakeSensor import FakeSensor
import socket
import ast
import time

# Global Variable
fakeSensorData = FakeSensor()
password = "CFT10"

def getInfo(con):
    # message sent to server                
    message = password    
    con.send(message.encode("utf-8"))
    
    # message received from server 
    data = con.recv(1024)
    
    # convert string list to list
    try:
        list = ast.literal_eval(data.decode("utf-8"))
        for warning in list:
            print(warning)            
    except:
        print(data.decode("utf-8"))
    
    con.close()
    print ("Connection has been closed")    
    
    # after N time call again
    time.sleep(15)
    Main()

def Main(): 
    # The remote host
    HOST = '127.0.0.1'
    # The same port as used by the server
    PORT = 50000
    # IPv4,tipo de socket   
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((HOST, PORT))
    print ("Connection has benn opened")    
    getInfo(tcp)
  
if __name__ == '__main__': 
    Main()