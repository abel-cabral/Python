## Vegetable Garden
I made this project to discipline of `Computer Network` during my graduate. We has a server
that receive object data from clients, server decide what's the best option to do and response that
with the instructions. My main idea here is, the senser in the client side send to server data about temperature,
humidity and others things related with earth quality. Server can decide if is need switch on water, for example.
There are three types of files: 
  - server: where all decision-making are executed.
  - vegetable: where sensor there is, sending status and waiting server response.
  - administrador: where just receive warnings about garden.

### Instructions
#### Download and install
- Python >= 3.6

## Running
- run server ```python3 server.py```
- run client vegetables for exemplo, ```python3 tomato.py```
- run administrator ```python3 admin.py```

## Meta
Abel C. Arruda – jcabral@id.uff.br
