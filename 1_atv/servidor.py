import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('localhost', 10001)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)

        while True:
            data = connection.recv(1024)
            dado_convertido = data.decode('utf-8').replace('\0', '')
            # print('-> recebido:', dict(dado_convertido))

            if data:
                connection.sendall(dado_convertido.encode())
            else:
                break
    finally:
        connection.close()
