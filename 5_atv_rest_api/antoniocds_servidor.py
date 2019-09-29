import datetime

from flask import Flask, abort, jsonify, make_response, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
api_endpoint = '/api/todo'


class Tarefa(object):
	__cont_id_tarefa = 1

	def __init__(self, nome: str, desc: str, concluida: bool):
		self.id = self.__cont_id_tarefa
		Tarefa.__cont_id_tarefa += 1
		self.data_criacao = datetime.datetime.now()
		self.nome = nome
		self.descricao = desc
		self.concluida = concluida if concluida is not None else False

	def converter_dict(self) -> dict:
		dic = {
			'nome': self.nome, 'id': self.id,
			'descricao': self.descricao, 'concluida': self.concluida,
			'data_criacao': self.data_criacao
		}

		return dic


colecao_tarefas = {
	1: Tarefa('Terminar exe de SD', 'Finalizar exe 2, 3 e 6', False),
	2: Tarefa('Dormir', 'Dormir mais que 3 horas', True)
}


# Exemplo de requisição (SO Linux e derivados):
# curl -i -X GET http://127.0.0.1:5000/api/todo/
@app.route(f"{api_endpoint}/", methods=['GET'])
def get_all():
	return jsonify([tar.converter_dict() for tar in colecao_tarefas.values()])


# Exemplo de requisição (SO Linux e derivados):
# curl -i -X GET http://127.0.0.1:5000/api/todo/1
@app.route(f"{api_endpoint}/<int:tarefa_id>", methods=['GET'])
def get_by_id(tarefa_id: int):
	tarefa = None

	if tarefa_id in colecao_tarefas:
		tarefa = colecao_tarefas[tarefa_id]

	else:
		abort(404, tarefa_id)

	return jsonify(tarefa.converter_dict())


# Exemplo de requisição (SO Linux e derivados):
# curl -i -X DELETE http://127.0.0.1:5000/api/todo/1
@app.route(f"{api_endpoint}/<int:tarefa_id>", methods=['DELETE'])
def delete(tarefa_id: int):
	tarefa = None

	if tarefa_id in colecao_tarefas:
		tarefa = colecao_tarefas[tarefa_id]

	else:
		abort(404, tarefa_id)

	del colecao_tarefas[tarefa_id]
	return '', 204


# Exemplo de requisição (SO Linux e derivados):
# curl -i -X POST -H 'Content-Type: application/json' -d '{"nome": "titulo tarefa", "descricao": "detalhes", "concluida": false}' http://127.0.0.1:5000/api/todo/
@app.route(f"{api_endpoint}/", methods=['POST'])
def post():
	# Se a requisição não tem um conteúdo OU não tem o nome da tarefa
	if not request.json or 'nome' not in request.json:
		abort(400)

	nova_tarefa = Tarefa(
		request.json['nome'],
		request.json['descricao'],
		request.json['concluida']
	)

	colecao_tarefas[nova_tarefa.id] = nova_tarefa

	return jsonify(nova_tarefa.converter_dict()), 201


# Exemplo de requisição (SO Linux e derivados):
# curl -i -X PUT -H 'Content-Type: application/json' -d '{"nome": "novo titulo", "descricao": "detalhes", "concluida": true}' http://127.0.0.1:5000/api/todo/1
@app.route(f"{api_endpoint}/<int:tarefa_id>", methods=['PUT'])
def put(tarefa_id: int):
	tarefa = None

	if tarefa_id in colecao_tarefas:
		tarefa = colecao_tarefas[tarefa_id]
		tarefa.concluida = request.json['concluida']
		tarefa.descricao = request.json['descricao']
		tarefa.nome = request.json['nome']

	else:
		abort(404, tarefa_id)

	return jsonify(tarefa.converter_dict()), 201


@app.errorhandler(404)
def not_found(error):
	msg = f'A tarefa de ID = {error.description} não foi encontrada'
	return make_response(jsonify({'erro': msg}), 404)


if __name__ == '__main__':
	app.run(debug=True)
