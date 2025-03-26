SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
 
DROP TABLE IF EXISTS alunos;

CREATE TABLE alunos (
    id_aluno (INT AUTO_INCREMENT PRIMARY KEY),
    nome_completo (VARCHAR(255) NOT NULL),
    data_nascimento (DATE NOT NULL),
    id_turma (FOREIGN KEY INT),
    nome_responsavel (VARCHAR(255) NOT NULL),
    telefone_responsavel (VARCHAR(20) NOT NULL),
    email_responsavel (VARCHAR(100) NOT NULL),
    informacoes_adicionais (TEXT),
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

CREATE TABLE turma (
  id_turma INT PRIMARY KEY AUTO_INCREMENT,
  nome_turma VARCHAR(50),
  id_professor INT,
  horario VARCHAR(100)
  FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);

CREATE TABLE professor (
  id_professor PRIMARY KEY INT AUTO_INCREMENT,
  nome_completo VARCHAR(255),
  email VARCHAR(100),
  telefone VARCHAR(20),
);

CREATE TABLE pagamento (
  id_pagamento PRIMARY KEY INT AUTO_INCREMENT,
  id_aluno INT,
  data_pagamento DATE,
  valor_pago DECIMAL(10,2),
  forma_pagamento VARCHAR(50),
  referencia VARCHAR(100),
  status VARCHAR(20),
  FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno//)
);

CREATE TABLE presenca (
  id_presenca PRIMARY KEY INT AUTO_INCREMENT,
  id_aluno INT,
  data_presenca DATE,
  presente BOOLEAN,
  FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

CREATE TABLE atividade (
  id_atividade PRIMARY KEY INT AUTO_INCREMENT,
  descricao TEXT,
  data_realizacao DATE
);

CREATE TABLE atividade_aluno (
  id_atividade INT,
  id_aluno INT,
  PRIMARY KEY (id_atividade, id_aluno),
  FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade),
  FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

CREATE TABLE usuario (
  id_usuario PRIMARY KEY INT AUTO_INCREMENT,
  login VARCHAR(50) UNIQUE,
  senha VARCHAR(255),
  nivel_acesso VARCHAR(20),
  id_professor INT,
  FOREIGN KEY (id_professor) REFERENCES professor(id_professor)
);