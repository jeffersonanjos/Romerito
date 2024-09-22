-- Exclui a tabela se ela já existir
DROP TABLE IF EXISTS user;

-- Cria a tabela com a definição correta para SQLite
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
