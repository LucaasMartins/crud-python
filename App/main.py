# main.py
from flask import Flask
from flasgger import Swagger
from App.cruProf import professor_bp
from App.crudAlunos import aluno_bp
from App.crudTurma import turma_bp

app = Flask(__name__)
swagger = Swagger(app)


app.register_blueprint(professor_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(turma_bp)

if __name__ == '__main__':
    app.run(debug=True)
