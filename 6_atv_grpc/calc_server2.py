#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from concurrent import futures

import grpc
import math

import calc_pb2_grpc
from calc_pb2 import UmArg, UmArgIntSemSinal, DoisArgs, Resposta, RespostaIntSemSinal


class Calc(calc_pb2_grpc.CalculadoraServicer):
	"""Serviço para realizar operações aritméticas"""

	def Somar(self, request: DoisArgs, context) -> Resposta:
		"""Soma o primeiro número com o segundo número, ex.: A + B

		:param request: Objeto contendo os dois números
		:param context: ???
		:return: O resultado da soma dos dois números
		"""
		return Resposta(resultado=request.num1 + request.num2)

	def Subtrair(self, request: DoisArgs, context) -> Resposta:
		"""Subtrai do primeiro número, o segundo número, ex: A - B

		:param request: Objeto contendo os dois números
		:param context: ???
		:return: O resultado da subtração dos dois números
		"""
		return Resposta(resultado=request.num1 - request.num2)

	def Multiplicar(self, request: DoisArgs, context) -> Resposta:
		"""Multiplica o primeiro número pelo segundo número, ex: A * B

		:param request: Objeto contendo os dois números
		:param context: ???
		:return: O resultado da multiplicação dos dois números
		"""
		return Resposta(resultado=request.num1 * request.num2)

	def Dividir(self, request: DoisArgs, context) -> Resposta:
		"""Divide (divisão real) o primeiro número pelo segundo número, ex: A / B

		:param request: Objeto contendo os dois números
		:param context: ???
		:return: O resultado da divisão dos dois números
		"""
		return Resposta(resultado=request.num1 / request.num2)

	def Potencia(self, request: DoisArgs, context) -> Resposta:
		"""Calcula a potência do primeiro número elevado ao segundo, ex: A ^ B

		:param request: Objeto contendo os dois números
		:param context: ???
		:return: O resultado da potenciação do primeiro pelo segundo
		"""
		return Resposta(resultado=request.num1 ** request.num2)

	def RaizQuad(self, request: UmArg, context) -> Resposta:
		"""Calcula a raiz quadrada do número de entrada

		:param request: Objeto contendo um único número real NÃO negativo
		:param context: ???
		:return: O resultado da radiciação quadrada do número de entrada
		"""
		return Resposta(resultado=request.num ** 0.5)

	def Fatorial(self, request: UmArgIntSemSinal, context) -> RespostaIntSemSinal:
		"""Calcula o fatorial do número INTEIRO de entrada

		:param request: Objeto contendo um único número inteiro NÃO negativo
		:param context: ???
		:return: O resultado do fatorial do número de entrada
		"""
		return RespostaIntSemSinal(resultado=math.factorial(request.num))


def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	calc_pb2_grpc.add_CalculadoraServicer_to_server(Calc(), server)
	server.add_insecure_port('[::]:50052')
	server.start()
	server.wait_for_termination()


if __name__ == '__main__':
	logging.basicConfig()
	serve()
