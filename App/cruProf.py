from flask import Blueprint, request, jsonify
import Util.bd as bd

prof_bp = Blueprint('professores', __name__)

@prof_bp.route('/professores', methods=['POST'])
def adicionar_professor():
    """
    Criar um novo professor
    ---
    tags:
      - Professores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome_completo
            - email
            - telefone
          properties:
            nome_completo:
              type: string
              example: "João Silva"
            email:
              type: string
              example: "joao@email.com"
            telefone:
              type: string
              example: "11999999999"
    responses:
      201:
        description: Professor criado com sucesso
      400:
        description: Dados inválidos
    """
    data = request.get_json()
    
    required_fields = ['nome_completo', 'email', 'telefone']
    
    if not all([field in data for field in required_fields]):
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        
        cursor.execute(
            """
            INSERT INTO professor (nome_completo, email, telefone)
            VALUES (%s, %s, %s)
            """,
            (data['nome_completo'], data['email'], data['telefone'])
        )
        conn.commit()
        return jsonify({"message": "Professor adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
@prof_bp.route('/professores/<int:id_professor>', methods=['GET'])
def read_professor(id_professor):
    """
    Buscar professor por ID
    ---
    tags:
      - Professores
    parameters:
      - name: id_professor
        in: path
        type: integer
        required: true
        description: ID do professor
    responses:
      200:
        description: Professor encontrado
      404:
        description: Professor não encontrado
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT * FROM professor WHERE id_professor = %s
            """,
            (id_professor,)
        )
        professor = cursor.fetchone()
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({
            "id_professor": professor[0],
            "nome_completo": professor[1],
            "email": professor[2],
            "telefone": professor[3],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
@prof_bp.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE professor
            SET nome_completo = %s, email = %s, telefone = %s
            WHERE id_professor = %s
            """,
            (data['nome_completo'], data['email'], data['telefone'],
             id_professor)
        )
        conn.commit()
        return jsonify({"message": "Professor atualizado"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
@prof_bp.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM professor WHERE id_professor = %s
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
        
