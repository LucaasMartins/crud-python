from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/pagamentos', methods=['POST'])
def adicionar_pagamento():
    data = request.get.json()

    required_fields = ['id_aluno', 'valor', 'data_pagamento', 'metodo_pagamento']

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
            INSERT INTO pagamentos (id_aluno, valor, data_pagamento, metodo_pagamento)
            VALUES (%s, %s, %s, %s)
            """,
            (data['id_aluno'], data['valor'], data['data_pagamento'], data['metodo_pagamento'])
        )
        conn.commit()
        return jsonify({"message": "Pagamento adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()