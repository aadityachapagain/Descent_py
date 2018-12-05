import socket

HOST, PORT = '127.0.0.1', 1200

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#refer to client.py
s.bind((HOST, PORT))
s.listen(2)#listen for 1 connection

conn, addr = s.accept()#start the actual data flow

print('connected to:', addr)

while 1:
    data = conn.recv(1024).decode('ascii')#receive 1024 bytes and decode using ascii
    print('client: '+data)
    if not data:
        break
    conn.send((data + ' [ addition by server ]').encode('ascii'))

conn.close()