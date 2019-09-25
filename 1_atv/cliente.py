import json
import socket

SIMB_COMANDO: str = "-> "
SIMB_ESPERA: str = "... "

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

end_server = ('localhost', 10001)
print(SIMB_COMANDO + 'conectado em - endereço: %s - porta: %s' % end_server)
sock.connect(end_server)

try:

    msg = {"a": 5, "b": 7, "op": "+"}
    print(SIMB_COMANDO + 'enviando dados: "%s"' % msg)

    msg_dumps = json.dumps({"a": 5, "b": 7, "op": "+"}).encode("utf-8")
    sock.sendall(msg_dumps)
    data = sock.recv(64)
    dado_convertido = json.loads(data.decode("utf-8"))

    print(SIMB_COMANDO + 'dados recebidos:', dado_convertido)

finally:
    sock.close()
