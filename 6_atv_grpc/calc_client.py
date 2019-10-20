#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time
from enum import Enum, auto

import grpc

import calc_pb2_grpc
from calc_pb2 import UmArg, UmArgIntSemSinal, DoisArgs


class EOperacaoAritmetica(Enum):
	DIVISAO = auto(),
	FATORIAL = auto(),
	MULTIPLICACAO = auto(),
	POTENCIA = auto(),
	RAIZ_QUAD = auto(),
	SOMA = auto(),
	SUBTRACAO = auto()


dict_digito_op = {
	1: ['SOMA', EOperacaoAritmetica.SOMA],
	2: ['SUBTRAÇÃO', EOperacaoAritmetica.SUBTRACAO],
	3: ['DIVISÃO', EOperacaoAritmetica.DIVISAO],
	4: ['MULTIPLICAÇÃO', EOperacaoAritmetica.MULTIPLICACAO],
	5: ['FATORIAL', EOperacaoAritmetica.FATORIAL],
	6: ['POTÊNCIA', EOperacaoAritmetica.POTENCIA],
	7: ['RAIZ QUADRADA', EOperacaoAritmetica.RAIZ_QUAD]
}


def imprimir_menu() -> None:
	"""Imprime o menu, a lista de operações e seus dígitos correspondentes"""
	print('\n- - - -> LISTA DE OPERAÇÕES DISPONÍVEIS <- - - -\n')

	for digito in range(1, len(dict_digito_op) + 1):
		print(f'Pressione {digito} - {dict_digito_op[digito][0]}')


def menu() -> EOperacaoAritmetica:
	"""Exibe menu e realiza a leitura da opção escolhida pelo usuário

	:return: Enum com a operação escolhida
	"""
	imprimir_menu()
	escolha = int(input('\nDigite a opção desejada: '))

	while escolha < 1 or escolha > 7:
		print(f'\n#ERRO: A operação de dígito {escolha} não existe!')
		imprimir_menu()
		escolha = int(input('\nDigite a opção desejada: '))

	return dict_digito_op[escolha][1]


def ler_num(real: bool, negativo: bool, msg: str = None):
	"""Realiza a leitura de um número inteiro ou real, positivo ou não.

	:param real: Flag que indica se número reais são aceitos
	:param negativo: Flag que indica se números negativos são permitidos
	:param msg: Mensagem para ser exibida na leitura do número
	:return: Um número inteirou ou flutuante, lido do teclado
	"""
	# Se não houver mensagem a ser exibida para entrada de dados, construa uma
	if msg is None or len(msg.strip()) < 1:
		str_tipo = 'REAL' if real else 'INTEIRO'
		str_negativo = ' NÃO negativo' if not negativo else ''
		msg = f'Digite um número {str_tipo}{str_negativo}: '

	num = float(input('\n' + msg))

	while (num < 0 and not negativo) or (num % 1 != 0 and not real):
		num = float(input('\nEntrada INVÁLIDA! ' + msg))

	return num if real else int(num)


def run():
	# Abra um canal de comunicação com o servidor
	with grpc.insecure_channel('localhost:1667') as channel:
		stub = calc_pb2_grpc.CalculadoraStub(channel)
		msg_n1 = 'Digite o primeiro número de entrada (ex.: -2.5): '
		msg_n2 = 'Digite o segundo número de entrada (ex.: 3): '
		entrada = None

		try:
			while 1:
				opcao: EOperacaoAritmetica = menu()
				stub_operacao = None

				if opcao == EOperacaoAritmetica.FATORIAL:
					entrada = UmArgIntSemSinal(
						num=ler_num(real=False, negativo=False)
					)
					stub_operacao = stub.Fatorial

				elif opcao == EOperacaoAritmetica.RAIZ_QUAD:
					entrada = UmArg(
						num=ler_num(real=True, negativo=False))
					stub_operacao = stub.RaizQuad

				else:
					entrada = DoisArgs(
						num1=ler_num(real=True, negativo=True, msg=msg_n1),
						num2=ler_num(real=True, negativo=True, msg=msg_n2)
					)

					if opcao == EOperacaoAritmetica.SOMA:
						stub_operacao = stub.Somar

					elif opcao == EOperacaoAritmetica.SUBTRACAO:
						stub_operacao = stub.Subtrair

					elif opcao == EOperacaoAritmetica.DIVISAO:
						stub_operacao = stub.Dividir

					elif opcao == EOperacaoAritmetica.MULTIPLICACAO:
						stub_operacao = stub.Multiplicar

					elif opcao == EOperacaoAritmetica.POTENCIA:
						stub_operacao = stub.Potencia

				crono_inic = time.time()
				resp = stub_operacao(entrada)
				crono_fim = time.time()

				print(f'\nResposta:\t{resp.resultado}')
				print(f'Duração:\t%.6f segundos' % (crono_fim - crono_inic))

		except KeyboardInterrupt:
			print('\n\n...Saindo!')


if __name__ == '__main__':
	logging.basicConfig()
	run()
