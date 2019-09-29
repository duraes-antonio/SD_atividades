import json
import re
import socket

SIMB_COMANDO: str = "-->\t"
SIMB_ESPERA: str = "...\t"


def calcular(expressao: str) -> float:
    nova_exp: str = expressao.replace("^", "**")
    return eval(nova_exp)


def validar_dado(dado: str) -> bool:
    pattern_num: str = r"^[+-]?\d+[!]?(\s*[\+\-\*\/\^]\s*[+-]?\d+[!]?)*"
    return re.match(pattern_num, dado) is not None


def main():
    # criação e configuração do socket e conexão
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_servidor = ('localhost', 10001)
    sock.bind(end_servidor)
    print(SIMB_COMANDO + 'executando - endereço: %s - porta: %s' % end_servidor)

    sock.listen(1)

    while True:
        print(f'\n{SIMB_ESPERA} esperando por clientes\n')
        conexao, end_cli = sock.accept()

        try:
            # Informe o endereço do cliente
            print(f'{SIMB_ESPERA} cliente ON - endereço: {end_cli[0]} - porta: {end_cli[1]}')

            while True:
                # Decodifique a mensagem com o padrão UTF-8
                data = conexao.recv(1024).decode("utf-8")

                # Se houver dados
                if data is not None and len(data) > 1:

                    # Converta o dado para JSON e imprima-o
                    dado_cvt = json.loads(data)
                    print(f'{SIMB_COMANDO} dado recebido:', dado_cvt)

                    # Valide o dado de entrada
                    retorno = None

                    if not validar_dado(dado_cvt):
                        retorno = "#ERRO: A expressão não possui um formato válido!"

                    else:
                        retorno = calcular(dado_cvt)

                    conexao.sendall(json.dumps(retorno).encode("utf-8"))

                else:
                    break

        finally:
            conexao.close()

    return 0


main()
