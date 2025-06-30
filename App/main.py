# main.py
from flask import Flask

app = Flask(__name__)

# Configuração do Swagger será adicionada após testar
try:
    from flasgger import Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Sistema Escolar API",
            "description": "API CRUD para gestão escolar",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"]
    }
    
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
    print("Swagger configurado com sucesso")
except ImportError:
    print("Swagger não disponível - continuando sem documentação")

# Importando e registrando os Blueprints
try:
    from crudAlunos import alunos_bp
    app.register_blueprint(alunos_bp)
except ImportError:
    print("Módulo crudAlunos não encontrado")

try:
    from cruProf import prof_bp
    app.register_blueprint(prof_bp)
except ImportError:
    print("Módulo cruProf não encontrado")

try:
    from crudUsuario import usuarios_bp
    app.register_blueprint(usuarios_bp)
except ImportError:
    print("Módulo crudUsuario não encontrado")

try:
    from crudTurma import turmas_bp
    app.register_blueprint(turmas_bp)
except ImportError:
    print("Módulo crudTurma não encontrado")

try:
    from crudPagamento import pagamentos_bp
    app.register_blueprint(pagamentos_bp)
except ImportError:
    print("Módulo crudPagamento não encontrado")

try:
    from crudPresenca import presencas_bp
    app.register_blueprint(presencas_bp)
except ImportError:
    print("Módulo crudPresenca não encontrado")

try:
    from crudAtividade import atividades_bp
    app.register_blueprint(atividades_bp)
except ImportError:
    print("Módulo crudAtividade não encontrado")

try:
    from crudAtividade_aluno import atividade_aluno_bp
    app.register_blueprint(atividade_aluno_bp)
except ImportError:
    print("Módulo crudAtividade_aluno não encontrado")

@app.route('/')
def home():
    return {"message": "API Sistema Escolar", "status": "running", "blueprints": len(app.blueprints)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)