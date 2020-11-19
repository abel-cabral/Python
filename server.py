# import socket programming library
from fakeSensor import FakeSensor
from threading import Thread
import socket

# import thread module
from _thread import *
import threading
import json

print_lock = threading.Lock()
        
password = "CFT10"
admin = ""
connection = []
connectionNumber = 0
adminMessages = []


def activerWater(sensor, index, time):
    fakeSensorData = sensor[1]  # Sensor data
    fakeSensorData.status = True
    fakeSensorData.time = time

    conn = sensor[0]
    json_data = json.dumps(fakeSensorData.__dict__, sort_keys=False, indent=2)
    conn.send(json_data.encode("utf-8"))
    connection.pop(index)


def engenier():    
    for i in range(len(connection)):
        fakeSensorData = connection[i][1]  # Sensor data
        # http://mundoprojetado.com.br/medindo-a-umidade-do-solo/
        umidade = int(fakeSensorData.metric)
        # 300 - Valores abaixo de 300 indicam que o solo está seco
        # 700 - Valores acima de 700 indicam que o solo está com a umidade ideal
                
        if(umidade <= 300):
            # Cria um alerta
            msg = "A planta " + \
                connection[i][1].id + \
                " esta com umidade abaixo de 300, verifique a integridade do vaso ou a mangueira de irrigação"
            adminMessages.append(msg)
            
            # Ativa a água
            activerWater(connection[i], i, 14)  # client connection
        elif(umidade > 300 and umidade < 700):
            # apenas molha
            activerWater(connection[i], i, 7)  # client connection
        else:
            # Não é necessario molhar
            json_data = json.dumps(
                fakeSensorData.__dict__, sort_keys=False, indent=2)
            connection[i][0].send(json_data.encode("utf-8"))
            connection.pop(i)
            return


def waitSensors(conn):
    while True:
        data = conn.recv(1024)  # Recebe os dados
        if not data:
            break

        # Check if is the admin
        if(data.decode("utf-8") == password):
            if (len(adminMessages) != 0):
                json_data = json.dumps(
                    adminMessages, sort_keys=False, indent=2)
                conn.send(json_data.encode("utf-8"))
                adminMessages.clear()
            else:
                conn.send("Não há avisos".encode("utf-8"))
        else:
            try:
                dataAndStatistic = []
                data = json.loads(data.decode("utf-8"))
                fakeSensorData = FakeSensor(
                    data["sensorType"], data["metric"], data["time"], data["message"], data["status"], data["id"])

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
    # IPv4,tipo de socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # garante que o socket será destruído (pode ser reusado) após uma interrupção da execução
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' +
              str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    s.listen(1)  # espera chegar pacotes na porta especificada

    while True:
        # Aceita conexões
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # Cria nova thread para uma nova conexão. O primeiro
    # argumento é o nome da função, e o segundo é uma tupla
    # com os parâmetros da função.
        start_new_thread(waitSensors, (conn,))
        i = i + 1


if __name__ == '__main__':
    Main()
