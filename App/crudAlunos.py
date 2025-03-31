from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO alunos (id_aluno, nome_completo, data_nascimento, nome_responsavel, telefone_responsavel,
            email_responsavel, informacoes_adicionais))
            VALUES (%s, %s, %s, %s, %s, %s, %s,)
            """,
            (data['id_aluno'], data['nome_completo'], data['data_nascimento'], data['nome_responsavel'], data['telefone_responsavel'], 
             data['email_responsavel'], data['informacoes_adicionais'])
        )
        conn.commit()
        return jsonify({"message": "Aluno adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno', methods=['GET'])
def read_aluno(id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM alunos WHERE id_aluno = %s
            """,
            (id_aluno,)
        )
        aluno = cursor.fetchone()
        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404
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
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE alunos
            SET nome_completo = %s, data_nascimento = %s, nome_responsavel = %s, telefone_reponsavel = %s, 
            email_reponsavel = %s, informacoes_adicionais = %s,
            WHERE aluno_id = %s
            """,
            (data['nome_completo'], data['data_nascimento'], data['nome_responsavel'], data['telefone_responsavel'], 
             data['email_responsavel'], data['informacoes_adicionais'], id_aluno)
        )
        conn.commit()
        return jsonify({"message": "Aluno atualizado"}), 200
    except Exception as e:  
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM alunos WHERE id_aluno = %s
            """,
            (id_aluno,)
        )
        conn.commit()
        return jsonify({"message": "Aluno deletado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
