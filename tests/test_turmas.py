import pytest
from unittest import mock

def test_get_turma(client, mocker):
    turma_mock = (1, "Turma A", 1, "08:00-10:00")
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = turma_mock
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/turmas/1')
    
    assert response.status_code == 200
    assert response.json['id_turma'] == 1
    assert response.json['nome_turma'] == "Turma A"
    assert response.json['id_professor'] == 1
    assert response.json['horario'] == "08:00-10:00"

def test_get_turma_nao_encontrada(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.get('/turmas/999')
    
    assert response.status_code == 404
    assert "não encontrada" in response.json['error']

def test_add_turma(client, mocker):
    nova_turma = {
        "nome_turma": "Turma B",
        "nome_completo": "João Silva",
        "horario": "14:00-16:00"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para encontrar o professor
    mock_cursor.fetchone.return_value = (1,)
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/turmas', json=nova_turma)
    
    assert response.status_code == 201
    assert "Turma adicionada com sucesso" in response.json['message']

def test_add_turma_professor_nao_encontrado(client, mocker):
    nova_turma = {
        "nome_turma": "Turma C",
        "nome_completo": "Professor Inexistente",
        "horario": "10:00-12:00"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Mock para não encontrar o professor
    mock_cursor.fetchone.return_value = None
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.post('/turmas', json=nova_turma)
    
    assert response.status_code == 404
    assert "Professor não encontrado" in response.json['error']

def test_update_turma(client, mocker):
    turma_atualizada = {
        "nome_turma": "Turma A Atualizada",
        "id_professor": 2,
        "horario": "09:00-11:00"
    }
    
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.put('/turmas/1', json=turma_atualizada)
    
    assert response.status_code == 200
    assert "Turma atualizada com sucesso" in response.json['message']

def test_delete_turma(client, mocker):
    mock_conn = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mocker.patch('Util.bd.create_connection', return_value=mock_conn)
    
    response = client.delete('/turmas/1')
    
    assert response.status_code == 200
    assert "Turma deletada com sucesso" in response.json['message']