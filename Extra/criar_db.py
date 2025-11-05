import sqlite3

# Conecta (ou cria) o banco de dados
conn = sqlite3.connect('pets.db')
cursor = conn.cursor()

# Cria a tabela de pets com os novos campos
cursor.execute('''
CREATE TABLE IF NOT EXISTS pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    raca TEXT NOT NULL,
    descricao TEXT,
    foto TEXT,
    responsavel TEXT,
    contato TEXT,
    adotado INTEGER DEFAULT 0,
    data_adocao TEXT
);
''')

# Cria a tabela de adoções
cursor.execute('''
CREATE TABLE IF NOT EXISTS adocoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER,
    nome_adotante TEXT,
    email TEXT,
    telefone TEXT,
    mensagem TEXT,
    data_adocao TEXT,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
);
''')

conn.commit()
conn.close()

print("✅ Banco de dados 'pets.db' criado/atualizado com sucesso!")
