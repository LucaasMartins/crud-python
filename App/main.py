# main.py
from flask import Flask
from flasgger import Swagger
from App.cruProf import professor_bp
from App.crudAlunos import aluno_bp
from App.crudTurma import turma_bp
from App.crudPagamento_corrigido import pagamento_bp
from App.importExport import import_export_bp
from App.importExport import import_export_bp

app = Flask(__name__)
swagger = Swagger(app)

# Registrando os blueprints
app.register_blueprint(professor_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(turma_bp)
app.register_blueprint(pagamento_bp)
app.register_blueprint(import_export_bp)

if __name__ == '__main__':
    app.run(debug=True)