import json
import socket

SIMB_COMANDO: str = "-> "
SIMB_ESPERA: str = "... "

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

end_servidor = ('localhost', 10001)
print(SIMB_COMANDO + 'executando - endereço: %s - porta: %s' % end_servidor)
sock.bind(end_servidor)
sock.listen(1)

while True:
    print(SIMB_ESPERA + 'esperando por clientes\n')
    conexao, end_cliente = sock.accept()

    try:
        print(SIMB_COMANDO + 'cliente conectado - endereço: %s - porta: %s:'
              % (end_cliente[0], end_cliente[1]))

        while True:
            data = conexao.recv(64).decode("utf-8")

            if data:
                dado_convertido = json.loads(data)
                print('-> recebido:', dado_convertido)
                print('-> tipo recebido:', type(dado_convertido))
                conexao.sendall(json.dumps(dado_convertido).encode("utf-8"))

            else:
                break

    finally:
        conexao.close()
