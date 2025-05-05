from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/atividade', methods=['POST'])
def adicionar_atividade():
    data = request.get_json()

    required_fields = ['id_turma', 'data_atividade', 'tipo_atividade', 'descricao_atividade', 'observacoes_atividade']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    cursor = bd.create_connection()
    if cursor is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    conn = cursor.cursor()
    try:
        cursor.execute("SELECT * FROM turmas WHERE id_turma = %s", (data['id_turma'],))
        turma = cursor.fetchone()

        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404

        cursor.execute(
            """
            INSERT INTO atividade (id_turma, data_atividade, tipo_atividade, descricao_atividade, observacoes_atividade)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['id_turma'], data['data_atividade'], data['tipo_atividade'], data['descricao_atividade'], data['observacoes_atividade'])
        )
        conn.commit()
        return jsonify({"message": "Atividade adicionada"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade/<int:id_atividade>', methods=['GET'])
def read_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM atividade WHERE id_atividade = %s
            """,
            (id_atividade,)
        )
        atividade = cursor.fetchone()
        if atividade is None:
            return jsonify({"error": "Atividade não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade[0],
            "id_turma": atividade[1],
            "data_atividade": atividade[2],
            "tipo_atividade": atividade[3],
            "descricao_atividade": atividade[4],
            "observacoes_atividade": atividade[5]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    data = request.get_json()

    required_fields = ['id_turma', 'data_atividade', 'tipo_atividade', 'descricao_atividade', 'observacoes_atividade']

    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400

    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE atividade
            SET id_turma = %s, data_atividade = %s, tipo_atividade = %s, descricao_atividade = %s, observacoes_atividade = %s
            WHERE id_atividade = %s
            """,
            (data['id_turma'], data['data_atividade'], data['tipo_atividade'], data['descricao_atividade'], data['observacoes_atividade'], id_atividade)
        )
        conn.commit()
        return jsonify({"message": "Atividade atualizada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/atividade/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM atividade WHERE id_atividade = %s
            """,
            (id_atividade,)
        )
        conn.commit()
        return jsonify({"message": "Atividade deletada"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)