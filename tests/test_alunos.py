import pytest
from unittest import mock

# Teste para obter um aluno existente
def test_get_aluno(client, mocker):
    aluno_mock = ("12345", "João da Silva", "Rua A, 123", "São Paulo", "SP", "01234567", "Brasil", "123456789")
    # Mocka o retorno do banco de dados
    mocker.patch('app.util.bd.create_connection', return_value=aluno_mock)
    
    response = client.get('/alunos/12345')
    
    assert response.status_code == 200
    assert response.json['aluno_id'] == '12345'
    assert response.json['nome'] == 'João da Silva'

# Teste para obter um aluno que não existe
def test_get_aluno_nao_encontrado(client):
    response = client.get('/alunos/99999')
    
    assert response.status_code == 404

# Teste para adicionar um novo aluno
def test_add_aluno(client, mocker):
    novo_aluno = {
        "aluno_id": "67890",
        "nome": "Maria Oliveira",
        "endereco": "Rua B, 456",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "cep": "12345678",
        "pais": "Brasil",
        "telefone": "987654321"
    }
    mocker.patch('app.util.bd.create_connection', return_value=None)
    
    response = client.post('/alunos', json=novo_aluno)
    
    assert response.status_code == 201
    assert response.json['aluno_id'] == '67890'
    assert response.json['nome'] == 'Maria Oliveira'

# Teste para atualizar um aluno existente
def test_update_aluno(client, mocker):
    aluno_atualizado = {
        "nome": "João da Silva Jr.",
        "endereco": "Rua A, 123",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01234567",
        "pais": "Brasil",
        "telefone": "123456789"
    }
    mocker.patch('app.util.bd.create_connection', return_value=None)
    
    response = client.put('/alunos/12345', json=aluno_atualizado)
    
    assert response.status_code == 200
    assert response.json['nome'] == 'João da Silva Jr.'

# Teste para deletar um aluno existente
def test_delete_aluno(client, mocker):
    mocker.patch('app.util.bd.create_connection', return_value=None)
    
    response = client.delete('/alunos/12345')
    
    assert response.status_code == 204