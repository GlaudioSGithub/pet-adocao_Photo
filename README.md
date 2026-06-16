1- Instalar o Flask:

pip install flask
python -m pip install flask


2- Estrutura:

pet-adocao/
├── app.py
├── static/
│   └── style.css
|   |__ upload/
├── templates/
│   ├── index.html
│   ├── cadastro.html
│   └── listar.html
└── pets.db

3- Criar DB:

import sqlite3

conn = sqlite3.connect('pets.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    raca TEXT NOT NULL,
    descricao TEXT
)
''')

conn.commit()
conn.close()

(Salvar e executar: python criar_db.py)

7- iniciar aplicação:
    flask run
    python app.py

8- **Executar a Aplicação**

Inicie o servidor:

python app.py

Acesse http://127.0.0.1:5000 no navegador.

9- Executar como Servidor local
    flask run --host=192.168.0.1 "IP da máquina"

# Adicionar a coluna data_adocao se não existir

import sqlite3

with sqlite3.connect('pets.db') as conn:
    cursor = conn.cursor()

    # Adicionar a coluna data_adocao se não existir
    cursor.execute('ALTER TABLE pets ADD COLUMN data_adocao TEXT')
    conn.commit()

print("Coluna 'data_adocao' adicionada com sucesso!")

# Apagar todos os registros

import sqlite3

with sqlite3.connect('pets.db') as conn:
    cursor = conn.cursor()
    # Apagar todos os registros
    cursor.execute('DELETE FROM pets')
    cursor.execute('DELETE FROM adocoes')
    # Resetar IDs
    cursor.execute('VACUUM')
    conn.commit()

print("Dados apagados e IDs resetados!")
