import json
import socket

SIMB_COMANDO: str = "-->\t"
SIMB_ESPERA: str = "...\t"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Endereço (127.0.0.1) e porta do servidor
end_server = ('localhost', 10001)
print(SIMB_COMANDO + 'conectado em - endereço: %s - porta: %s' % end_server)
sock.connect(end_server)

try:

    # Cria pacote com os operadores e o operando
    msg = "2 ^ 2.87 + 3.1"
    print(SIMB_ESPERA + 'enviando dados: "%s"' % msg)

    msg_dumps = json.dumps(msg).encode("utf-8")
    sock.sendall(msg_dumps)
    data = sock.recv(1024)
    dado_convertido = json.loads(data.decode("utf-8"))

    print(SIMB_COMANDO + 'dados recebidos:', dado_convertido)

finally:
    sock.close()
