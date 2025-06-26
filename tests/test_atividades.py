import pytest
from unittest import mock

def test_get_atividade(client, mocker):
    atividade_mock = (1, 1, "2023-06-01", "prova", "Prova de matemática", "Primeira avaliação")
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = atividade_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/atividade/1')
    
    assert response.status_code == 200
    assert response.json['id_atividade'] == 1
    assert response.json['id_turma'] == 1
    assert response.json['tipo_atividade'] == "prova"
    assert response.json['descricao_atividade'] == "Prova de matemática"

def test_get_atividade_nao_encontrada(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/atividade/999')
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']

def test_add_atividade(client, mocker):
    nova_atividade = {
        "id_turma": 1,
        "data_atividade": "2023-06-01",
        "tipo_atividade": "exercicio",
        "descricao_atividade": "Lista de exercícios",
        "observacoes_atividade": "Para casa"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para encontrar a turma
    mock_cursor.fetchone.return_value = (1, "Turma A")
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/atividade', json=nova_atividade)
    
    assert response.status_code == 201
    assert "Atividade adicionada" in response.json['message']

def test_add_atividade_campos_obrigatorios(client):
    atividade_incompleta = {
        "id_turma": 1,
        "data_atividade": "2023-06-01"
        # Faltando outros campos obrigatórios
    }
    
    response = client.post('/atividade', json=atividade_incompleta)
    
    assert response.status_code == 400
    assert "Campos obrigatórios" in response.json['error']

def test_add_atividade_turma_nao_encontrada(client, mocker):
    nova_atividade = {
        "id_turma": 999,
        "data_atividade": "2023-06-01",
        "tipo_atividade": "exercicio",
        "descricao_atividade": "Lista de exercícios",
        "observacoes_atividade": "Para casa"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para não encontrar a turma
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/atividade', json=nova_atividade)
    
    assert response.status_code == 404
    assert "Turma não encontrada" in response.json['error']

def test_update_atividade(client, mocker):
    atividade_atualizada = {
        "id_turma": 1,
        "data_atividade": "2023-06-02",
        "tipo_atividade": "prova",
        "descricao_atividade": "Prova final",
        "observacoes_atividade": "Avaliação final"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/atividade/1', json=atividade_atualizada)
    
    assert response.status_code == 200
    assert "Atividade atualizada" in response.json['message']

def test_delete_atividade(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/atividade/1')
    
    assert response.status_code == 200
    assert "Atividade deletada" in response.json['message']