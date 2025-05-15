import pytest
from flask import Flask
import sys
import os

# Adiciona o diretório raiz do projeto ao path para importar os módulos corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from App.cruProf import professor_bp
from App.crudAlunos import app as alunos_app
from App.crudTurma import turma_bp
from App.crudPagamento_corrigido import pagamento_bp

@pytest.fixture
def app():
    """Cria e configura uma instância Flask para testes."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Registra os blueprints
    app.register_blueprint(professor_bp)
    app.register_blueprint(turma_bp)
    app.register_blueprint(pagamento_bp)
    
    # Para o módulo de alunos que não usa blueprint
    for rule in alunos_app.url_map.iter_rules():
        app.add_url_rule(rule.rule, rule.endpoint, alunos_app.view_functions[rule.endpoint], methods=rule.methods)
    
    return app

@pytest.fixture
def client(app):
    """Um cliente de teste para o app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Um runner de teste para os comandos CLI do app."""
    return app.test_cli_runner()