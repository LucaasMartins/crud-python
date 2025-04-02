from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/turmas', methods=['POST'])
def adicionar_turma():
    data = request.get_json()