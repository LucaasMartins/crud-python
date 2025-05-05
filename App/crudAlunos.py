import logging
from flask import Flask, request, jsonify
import psycopg2
import yaml

# Configuração do sistema de log
logging.basicConfig(
    filename='escola_infantil.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

def create_connection():
    try:
        with open('Util/paramsBD.yml', 'r') as file:
            config = yaml.safe_load(file)
        connection = psycopg2.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['database']
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()

    # Validação de campos obrigatórios
    required_fields = ['nome_completo', 'data_nascimento', 'id_turma', 'nome_responsavel',
                       'telefone_responsavel', 'email_responsavel']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logging.warning(f"CREATE: Campos obrigatórios ausentes: {', '.join(missing_fields)}")
        return jsonify({"error": f"Campos obrigatórios não preenchidos: {', '.join(missing_fields)}"}), 400

    conn = create_connection()
    if conn is None:
        logging.error("CREATE: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM turmas WHERE id_turma = %s", (data['id_turma'],))
        turma = cursor.fetchone()

        if turma is None:
            logging.warning(f"CREATE: Turma com ID {data['id_turma']} não encontrada.")
            return jsonify({"error": "Turma não encontrada"}), 404

        cursor.execute(
            """
            INSERT INTO alunos (nome_completo, data_nascimento, nome_responsavel, telefone_responsavel,
            email_responsavel, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_aluno
            """,
            (data['nome_completo'], data['data_nascimento'], data['nome_responsavel'], data['telefone_responsavel'], 
             data['email_responsavel'], data.get('informacoes_adicionais', ''))
        )
        id_aluno = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"CREATE: Aluno {data['nome_completo']} inserido com sucesso. ID gerado: {id_aluno}")
        return jsonify({"message": "Aluno adicionado", "id_aluno": id_aluno}), 201
    except IntegrityError as e:
        conn.rollback()
        logging.error(f"CREATE: Erro de integridade ao inserir aluno - {str(e)}")
        return jsonify({"error": "Erro de integridade ao inserir aluno"}), 400
    except Exception as e:
        conn.rollback()
        logging.error(f"CREATE: Erro ao inserir aluno - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def read_aluno(id_aluno):
    conn = create_connection()
    if conn is None:
        logging.error("READ: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (id_aluno,))
        aluno = cursor.fetchone()
        if aluno is None:
            logging.warning(f"READ: Aluno com ID {id_aluno} não encontrado.")
            return jsonify({"error": "Aluno não encontrado"}), 404

        logging.info(f"READ: Aluno com ID {id_aluno} consultado com sucesso.")
        return jsonify({
            "id_aluno": aluno[0],
            "nome_completo": aluno[1],
            "data_nascimento": aluno[2],
            "nome_responsavel": aluno[3],
            "telefone_responsavel": aluno[4],
            "email_responsavel": aluno[5],
            "informacoes_adicionais": aluno[6],
        }), 200
    except Exception as e:
        logging.error(f"READ: Erro ao consultar aluno com ID {id_aluno} - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    data = request.get_json()
    conn = create_connection()
    if conn is None:
        logging.error("UPDATE: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE alunos
            SET nome_completo = %s, data_nascimento = %s, nome_responsavel = %s, telefone_responsavel = %s, 
            email_responsavel = %s, informacoes_adicionais = %s
            WHERE id_aluno = %s
            """,
            (data['nome_completo'], data['data_nascimento'], data['nome_responsavel'], data['telefone_responsavel'], 
             data['email_responsavel'], data.get('informacoes_adicionais', ''), id_aluno)
        )
        if cursor.rowcount == 0:
            logging.warning(f"UPDATE: Aluno com ID {id_aluno} não encontrado.")
            return jsonify({"error": "Aluno não encontrado"}), 404

        conn.commit()
        logging.info(f"UPDATE: Aluno com ID {id_aluno} atualizado com sucesso.")
        return jsonify({"message": "Aluno atualizado"}), 200
    except Exception as e:
        conn.rollback()
        logging.error(f"UPDATE: Erro ao atualizar aluno com ID {id_aluno} - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    conn = create_connection()
    if conn is None:
        logging.error("DELETE: Falha ao conectar ao banco de dados.")
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM alunos WHERE id_aluno = %s", (id_aluno,))
        if cursor.rowcount == 0:
            logging.warning(f"DELETE: Aluno com ID {id_aluno} não encontrado.")
            return jsonify({"error": "Aluno não encontrado"}), 404

        conn.commit()
        logging.info(f"DELETE: Aluno com ID {id_aluno} removido com sucesso.")
        return jsonify({"message": "Aluno deletado"}), 200
    except Exception as e:
        conn.rollback()
        logging.error(f"DELETE: Erro ao deletar aluno com ID {id_aluno} - {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
