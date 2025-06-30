from flask import Blueprint, request, jsonify
import Util.bd as bd

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/turmas', methods=['POST'])
def adicionar_turma():
    """
    Criar uma nova turma
    ---
    tags:
      - Turmas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome_completo
            - nome_turma
            - horario
          properties:
            nome_completo:
              type: string
              example: "João Silva"
              description: Nome do professor responsável
            nome_turma:
              type: string
              example: "Turma A"
            horario:
              type: string
              example: "08:00-12:00"
    responses:
      201:
        description: Turma criada com sucesso
      400:
        description: Dados inválidos
      404:
        description: Professor não encontrado
    """
    data = request.get_json()
    
    required_fields = ['nome_completo', 'nome_turma', 'horario']
    
    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_professor FROM professor WHERE nome_completo = %s", (data['nome_completo'],))
        professor = cursor.fetchone()
        
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        
        id_professor = professor[0]
        
        cursor.execute(
            """
            INSERT INTO turma (nome_turma, id_professor, horario)
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
        
@turmas_bp.route('/turmas/<int:id_turma>', methods=['GET'])
def read_turma(id_turma):
    """
    Buscar turma por ID
    ---
    tags:
      - Turmas
    parameters:
      - name: id_turma
        in: path
        type: integer
        required: true
        description: ID da turma
    responses:
      200:
        description: Turma encontrada
      404:
        description: Turma não encontrada
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM turma WHERE id_turma = %s
            """,
            (id_turma,)
        )
        turma = cursor.fetchone()
        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({
            "id_turma": turma[0],
            "nome_turma": turma[1],
            "id_professor": turma[2],
            "horario": turma[3],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@turmas_bp.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE turma
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s
            """,
            (data['nome_turma'], data['id_professor'],
             data['horario'], id_turma)
        )
        conn.commit()
        return jsonify({"message": "Turma atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@turmas_bp.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM turma WHERE id_turma = %s
            """,
            (id_turma,)
        )
        conn.commit()
        return jsonify({"message": "Turma deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

