from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/atividade_aluno', methods=['POST'])
def adicionar_atividade_aluno():
    data = request.get_json()

    required_fields = ['id_aluno', 'id_atividade', 'data_atividade', 'tipo_atividade', 'descricao_atividade', 'observacoes_atividade']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    cursor = bd.create_connection()
    if cursor is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    conn = cursor.cursor()
    try:
        cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (data['id_aluno'],))
        aluno = cursor.fetchone()

        if aluno is None:
            return jsonify({"error": "Aluno não encontrado"}), 404

        cursor.execute(
            """
            INSERT INTO atividade_aluno (id_aluno, id_atividade, data_atividade, tipo_atividade, descricao_atividade, observacoes_atividade)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data['id_aluno'], data['id_atividade'], data['data_atividade'], data['tipo_atividade'], data['descricao_atividade'], data['observacoes_atividade'])
        )
        conn.commit()
        return jsonify({"message": "Atividade do aluno adicionada"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade_aluno>', methods=['GET'])
def read_atividade_aluno(id_atividade_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM atividade_aluno WHERE id_atividade_aluno = %s
            """,
            (id_atividade_aluno,)
        )
        atividade_aluno = cursor.fetchone()
        if atividade_aluno is None:
            return jsonify({"error": "Atividade do aluno não encontrada"}), 404
        return jsonify({
            "id_atividade_aluno": atividade_aluno[0],
            "id_aluno": atividade_aluno[1],
            "id_atividade": atividade_aluno[2],
            "data_atividade": atividade_aluno[3],
            "tipo_atividade": atividade_aluno[4],
            "descricao_atividade": atividade_aluno[5],
            "observacoes_atividade": atividade_aluno[6]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade_aluno>', methods=['PUT'])
def update_atividade_aluno(id_atividade_aluno):
    data = request.get_json()

    required_fields = ['id_aluno', 'id_atividade', 'data_atividade', 'tipo_atividade', 'descricao_atividade', 'observacoes_atividade']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400

    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade_aluno WHERE id_atividade_aluno = %s", (id_atividade_aluno,))
        atividade_aluno = cursor.fetchone()

        if atividade_aluno is None:
            return jsonify({"error": "Atividade do aluno não encontrada"}), 404

        cursor.execute(
            """
            UPDATE atividade_aluno
            SET id_aluno = %s, id_atividade = %s, data_atividade = %s, tipo_atividade = %s, descricao_atividade = %s, observacoes_atividade = %s
            WHERE id_atividade_aluno = %s
            """,
            (data['id_aluno'], data['id_atividade'], data['data_atividade'], data['tipo_atividade'], data['descricao_atividade'], data['observacoes_atividade'], id_atividade_aluno)
        )
        conn.commit()
        return jsonify({"message": "Atividade do aluno atualizada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade_aluno/<int:id_atividade_aluno>', methods=['DELETE'])
def delete_atividade_aluno(id_atividade_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM atividade_aluno WHERE id_atividade_aluno = %s", (id_atividade_aluno,))
        atividade_aluno = cursor.fetchone()

        if atividade_aluno is None:
            return jsonify({"error": "Atividade do aluno não encontrada"}), 404

        cursor.execute(
            """
            DELETE FROM atividade_aluno WHERE id_atividade_aluno = %s
            """,
            (id_atividade_aluno,)
        )
        conn.commit()
        return jsonify({"message": "Atividade do aluno deletada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)