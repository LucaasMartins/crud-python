from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/professores', methods=['POST'])
def adicionar_professor():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO professores (nome_completo, data_nascimento, disciplina, telefone, email, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data['nome_completo'], data['data_nascimento'], data['disciplina'], data['telefone'], 
             data['email'], data['informacoes_adicionais'])
        )
        conn.commit()
        return jsonify({"message": "Professor adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['GET'])
def read_professor(id_professor):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM professores WHERE id_professor = %s
            """,
            (id_professor,)
        )
        professor = cursor.fetchone()
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({
            "id_professor": professor[0],
            "nome_completo": professor[1],
            "data_nascimento": professor[2],
            "disciplina": professor[3],
            "telefone": professor[4],
            "email": professor[5],
            "informacoes_adicionais": professor[6],
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE professores
            SET nome_completo = %s, data_nascimento = %s, disciplina = %s, telefone = %s, 
            email = %s, informacoes_adicionais = %s
            WHERE id_professor = %s
            """,
            (data['nome_completo'], data['data_nascimento'], data['disciplina'], data['telefone'], 
             data['email'], data['informacoes_adicionais'], id_professor)
        )
        conn.commit()
        return jsonify({"message": "Professor atualizado"}), 200
    except Exception as e:  
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM professores WHERE id_professor = %s
            """,
            (id_professor,)
        )
        conn.commit()
        return jsonify({"message": "Professor deletado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)