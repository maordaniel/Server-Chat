#server
import socket
import select
import threading

server = socket.socket()
server.bind(("192.168.1.28", 1))
server.listen(5)
inputs = [server]
users = {}
names = []
print("starting server..")

def notify_all(msg, non_receptors):
    for connection in inputs:
        if connection not in non_receptors:
            connection.send(msg)

def greet(address,client):
    global users
    greetMsg = f"hello {users[address][0]}! \n users online: "
    users[address][1].send(greetMsg.encode())
    try:
        for i in range(len(names)):
            if names[i] == users[address][0]:
                pass
            else:
                ms = f'[{str(i+ 1) + "- " + names[i]}]'
                users[address][1].send(ms.encode())
        notify_all(f"\nclient {users[address][0]} enterd".encode(), [server, users[address][1]])
    except:
        pass



def name():
    global s
    client, address = server.accept()
    msg = "please enter your name:"
    msg_1 = "This name is already taken"
    client.send(msg.encode())
    s = [address]
    for i in s:
        if i not in users.keys():
            inputs.append(client)
            users[i] = [client.recv(1024).decode()]
            users[i] += [client]
            if users[i][0] in names:
                users[i][1].send(msg_1.encode())
                while True:
                    users[i][0] = client.recv(1024).decode()
                    if users[i][0] not in names:
                        names.append(users[i][0])
                        greet(address,client)
                        break
                    else:
                        client.send(msg_1.encode())
                        continue
            else:
                names.append(users[i][0])
                greet(address,client)


while inputs:
    r, _,_ = select.select(inputs, [], [])
    for i in r:
        if i is server:
            try:
                t = threading.Thread(target=name)
                t.start()
            except:
                pass
        else:
            try:
                print('-')
                data = i.recv(1024)
                notify_all(str(str(users[i.getpeername()][0]) + ">>> " + data.decode()).encode(), [server, i])

            except:
                try:
                    inputs.remove(i)
                    print(f"client {users[i.getpeername()][0]} BYE")
                    notify_all(f"client {users[i.getpeername()][0]} left".encode(), [server])
                    del users[i.getpeername()]
                    i.close()
                except:
                    pass
