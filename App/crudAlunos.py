from flask import Blueprint, request, jsonify
import Util.bd as bd

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/alunos', methods=['POST'])
def adicionar_aluno():
    """
    Criar um novo aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome_completo
            - data_nascimento
            - id_turma
            - nome_responsavel
            - telefone_responsavel
            - email_responsavel
          properties:
            nome_completo:
              type: string
              example: "Maria Santos"
            data_nascimento:
              type: string
              format: date
              example: "2010-05-15"
            id_turma:
              type: integer
              example: 1
            nome_responsavel:
              type: string
              example: "Ana Santos"
            telefone_responsavel:
              type: string
              example: "11888888888"
            email_responsavel:
              type: string
              example: "ana@email.com"
            informacoes_adicionais:
              type: string
              example: "Observações gerais"
    responses:
      201:
        description: Aluno criado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Turma não encontrada
    """
    data = request.get_json()

    required_fields = ['nome_completo', 'data_nascimento', 'id_turma', 'nome_responsavel',
                       'telefone_responsavel', 'email_responsavel']
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Campos obrigatórios não preenchidos: {', '.join(missing_fields)}"}), 400

    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Connection to DB failed"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM turma WHERE id_turma = %s", (data['id_turma'],))
        turma = cursor.fetchone()

        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404

        cursor.execute(
            """
            INSERT INTO alunos (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel,
            email_responsavel, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (data['nome_completo'], data['data_nascimento'], data['id_turma'], data['nome_responsavel'], data['telefone_responsavel'], 
             data['email_responsavel'], data.get('informacoes_adicionais', ''))
        )
        conn.commit()
        return jsonify({"message": "Aluno adicionado"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
def read_aluno(id_aluno):
    """
    Buscar aluno por ID
    ---
    tags:
      - Alunos
    parameters:
      - name: id_aluno
        in: path
        type: integer
        required: true
        description: ID do aluno
    responses:
      200:
        description: Aluno encontrado
      404:
        description: Aluno não encontrado
    """
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
            "id_turma": aluno[3],
            "nome_responsavel": aluno[4],
            "telefone_responsavel": aluno[5],
            "email_responsavel": aluno[6],
            "informacoes_adicionais": aluno[7],
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
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
            SET nome_completo = %s, data_nascimento = %s, id_turma = %s, nome_responsavel = %s, telefone_responsavel = %s, 
            email_responsavel = %s, informacoes_adicionais = %s
            WHERE id_aluno = %s
            """,
            (data['nome_completo'], data['data_nascimento'], data['id_turma'], data['nome_responsavel'], data['telefone_responsavel'], 
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

@alunos_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
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


