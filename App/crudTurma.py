from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/turmas', methods=['POST'])
def adicionar_turma():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_professor FROM professores WHERE nome_completo = %s", (data['nome_completo'],))
        professor = cursor.fetchone()
        
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        
        id_professor = professor[0]
        
        cursor.execute(
            """
            INSERT INTO turmas (nome_turma, id_professor, horario)
            VALUES (%s, %s, %s)
            """,
            (data['nome_turma'], id_professor, data['horario'])
        )
        conn.commit()
        return jsonify({"message": "Turma adicionada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        