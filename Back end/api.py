from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# Test Base do servidor rodando
@app.route('/', methods=['GET'])
def TEST():
    return jsonify({'mensagem': 'ON '}), 200

app.debug = True

# Configurações do banco de dados
connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='04466038058',
    database='database_RGE',
    autocommit=True
)

# Rota para criar um novo registro
@app.route('/registros', methods=['POST'])
def criar_registro():
    dados = request.get_json()

    nome = dados['nome']
    ure = dados['ure']
    equipe = dados['equipe']
    material = dados['material']
    quantidade = dados['quantidade']
    unidade = dados['unidade']
    justificativa = dados['justificativa']

    try:
        cursor = connection.cursor()

        query = "INSERT INTO Pedidos (nome, ure, equipe, material, quantidade, unidade, justificativa) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (nome, ure, equipe, material, quantidade, unidade, justificativa)

        print(values)  # Imprime os dados recebidos no console para verificação
        cursor.execute(query, values)

        # Adiciona os cabeçalhos à resposta para permitir todas as origens e métodos HTTP
        response = jsonify({'mensagem': 'Registro criado com sucesso'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        return response, 201

    except Exception as e:
        # Adiciona os cabeçalhos à resposta para permitir todas as origens e métodos HTTP
        response = jsonify({'mensagem': 'Erro ao criar registro', 'erro': str(e)})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        return response, 500

# Rota para obter todos os registros
@app.route('/registros', methods=['GET'])
def obter_registros():
    try:
        cursor = connection.cursor()

        query = "SELECT * FROM Pedidos"

        cursor.execute(query)
        registros = cursor.fetchall()

     
       

        # Converter registros para um formato adequado para JSON (opcional)
        registros_json = []
        for registro in registros:
            registro_json = {
                'id': registro[0],
                'nome': registro[1],
                'ure': registro[2],
                'equipe': registro[3],
                'material': registro[4],
                'quantidade': registro[5],
                'unidade': registro[6],
                'justificativa': registro[7]
            }
            registros_json.append(registro_json)

        return jsonify(registros_json), 200

    except Exception as e:
        return jsonify({'mensagem': 'Erro ao obter registros', 'erro': str(e)}), 500

# Rota para obter um registro específico
@app.route('/registros/<int:registro_id>', methods=['GET'])
def obter_registro(registro_id):
    try:
        cursor = connection.cursor()

        query = "SELECT * FROM Pedidos WHERE id = %s"
        values = (registro_id)

        cursor.execute(query, values)
        registro = cursor.fetchone()


        if registro is None:
            return jsonify({'mensagem': 'Registro não encontrado'}), 404

        registro_json = {
            'id': registro[0],
            'nome': registro[1],
            'ure': registro[2],
            'equipe': registro[3],
            'material': registro[4],
            'quantidade': registro[5],
            'unidade': registro[6],
            'justificativa': registro[7]
        }

        

        return jsonify(registro_json), 200

    except Exception as e:
        return jsonify({'mensagem': 'Erro ao obter registro', 'erro': str(e)}), 500

# Rota para atualizar um registro
@app.route('/registros/<int:registro_id>', methods=['PUT'])
def atualizar_registro(registro_id):
    dados = request.get_json()
    nome = dados['nome']
    ure = dados['ure']
    equipe = dados['equipe']
    material = dados['material']
    quantidade = dados['quantidade']
    unidade = dados['unidade']
    justificativa = dados['justificativa']

    try:
        cursor = connection.cursor()

        query = "UPDATE Pedidos SET nome = %s, ure = %s, equipe = %s, material = %s, quantidade = %s, unidade = %s, justificativa = %s WHERE id = %s"
        values = (nome, ure, equipe, material, quantidade, unidade, justificativa, registro_id)

        cursor.execute(query, values)

        return jsonify({'mensagem': 'Registro atualizado com sucesso'}), 200

    except Exception as e:
        return jsonify({'mensagem': 'Erro ao atualizar registro', 'erro': str(e)}), 500

# Rota para excluir um registro
@app.route('/registros/<int:registro_id>', methods=['DELETE'])
def excluir_registro(registro_id):
    try:
        cursor = connection.cursor()

        query = "DELETE FROM Pedidos WHERE id = %s"
        values = (registro_id)

        cursor.execute(query, values)

        return jsonify({'mensagem': 'Registro excluído com sucesso'}), 200

    except Exception as e:
        return jsonify({'mensagem': 'Erro ao excluir registro', 'erro': str(e)}), 500


if __name__ == '__main__':
    app.run()
