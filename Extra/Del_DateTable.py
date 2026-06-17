import sqlite3

#with sqlite3.connect('pets.db') as conn:
#    cursor = conn.cursor()
#    # Apagar todos os dados das tabelas
#    cursor.execute('DELETE FROM pets')  # Limpar a tabela pets
#    cursor.execute('DELETE FROM adocoes')  # Limpar a tabela adocoes
#    conn.commit()

#print("Dados apagados com sucesso!")

conn = sqlite3.connect('pets.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(pets)")
print(cursor.fetchall())
conn.close()
