import pickle
import socket

SIMB_COMANDO: str = "-> "
SIMB_ESPERA: str = "... "

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

end_server = ('localhost', 10001)
print(SIMB_COMANDO + ' conectado em - endereço: %s - porta: %s' % end_server)
sock.connect(end_server)

try:

    msg = {"a": 5, "b": 7, "op": "+"}
    print(SIMB_COMANDO + 'enviando dados "%s"' % msg)

    msg_dumps = pickle.dumps(msg)
    msg_encod = bytes(f'{len(msg):<{1024}}', "utf-8") + msg_dumps
    sock.sendall(bytes(msg_encod, "utf-8"))

    bytes_recebidos = 0
    bytes_esperados = 1024
    while bytes_recebidos < bytes_esperados:
        data = sock.recv(1024)
        bytes_recebidos += len(data)

        # TODO: Decodificar corretamente (https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/)
        print(SIMB_COMANDO + 'dados recebidos:', pickle.loads(data))

finally:
    sock.close()
