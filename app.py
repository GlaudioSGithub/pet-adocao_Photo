from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Definir o diretório para salvar as imagens
UPLOAD_FOLDER = 'static/uploads'  # Pasta para armazenar imagens

# Definir tipos permitidos para o upload (imagens)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para verificar se a extensão é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ===== Página inicial =====
@app.route('/')
def index():
    return render_template('index.html')


# Página para cadastrar e editar pets
@app.route('/adicionar', methods=['GET', 'POST'])
@app.route('/adicionar/<int:id>', methods=['GET', 'POST'])
def adicionar_pet(id=None):
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        raca = request.form['raca']
        descricao = request.form['descricao']
        responsavel = request.form['responsavel']
        contato = request.form['contato']
        foto = request.files['foto']

        # Verifica se uma foto foi enviada
        foto = request.files.get('foto')
        foto_path = None

        if foto and allowed_file(foto.filename):
            # Cria o diretório se não existir
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Garante um nome único
            foto_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(foto.filename)}"
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_filename)
            foto.save(foto_path)

        # Conexão com o banco de dados SQLite
        with sqlite3.connect('pets.db') as conn:
            cursor = conn.cursor()

            if id:  # Caso seja edição
                if foto_path:
                    cursor.execute("UPDATE pets SET nome=?, idade=?, raca=?, descricao=?, foto=? WHERE id=?", 
                                   (nome, idade, raca, descricao, foto_path, id))
                else:
                    cursor.execute("UPDATE pets SET nome=?, idade=?, raca=?, descricao=? WHERE id=?", 
                                   (nome, idade, raca, descricao, id))
            else:  # Caso seja adição
                cursor.execute("INSERT INTO pets (nome, idade, raca, descricao, foto) VALUES (?, ?, ?, ?, ?)", 
                               (nome, idade, raca, descricao, foto_path))

            conn.commit()

        return redirect('/listar')

    # Para modo edição
    pet = None
    if id:
        with sqlite3.connect('pets.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pets WHERE id=?", (id,))
            pet = cursor.fetchone()

    return render_template('adicionar.html', pet=pet)

# Rota para buscar pets
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    pets = []
    if request.method == 'POST':
        termo = request.form['termo']
        with sqlite3.connect('pets.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM pets WHERE nome LIKE ? OR raca LIKE ?', (f'%{termo}%', f'%{termo}%'))
            pets = cursor.fetchall()

    return render_template('buscar.html', pets=pets)


# Página para confirmar exclusão
@app.route('/excluir/<int:pet_id>', methods=['GET'])
def confirmar_exclusao(pet_id):
    with sqlite3.connect('pets.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pets WHERE id = ?', (pet_id,))
        pet = cursor.fetchone()

    return render_template('excluir.html', pet=pet)

# Rota para excluir um pet após confirmação
@app.route('/excluir/<int:pet_id>', methods=['POST'])
def excluir(pet_id):
    with sqlite3.connect('pets.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pets WHERE id = ?', (pet_id,))
        conn.commit()

    return redirect('/listar')  # Redireciona para a lista após exclusão bem-sucedida


# Rota para editar um pet
@app.route('/editar/<int:pet_id>', methods=['GET', 'POST'])
def editar(pet_id):
    with sqlite3.connect('pets.db') as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            nome = request.form['nome']
            idade = request.form['idade']
            raca = request.form['raca']
            descricao = request.form['descricao']
            responsavel = request.form['responsavel']
            contato = request.form['contato']
            foto = request.files.get('foto')
            foto_path = None

            if foto and allowed_file(foto.filename):
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                foto_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(foto.filename)}"
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_filename)
                foto.save(foto_path)

                cursor.execute('''
                    UPDATE pets
                    SET nome=?, idade=?, raca=?, descricao=?, responsavel=?, contato=?, foto=?
                    WHERE id=?
                ''', (nome, idade, raca, descricao, responsavel, contato, foto_path, pet_id))
            else:
                cursor.execute('''
                    UPDATE pets
                    SET nome=?, idade=?, raca=?, descricao=?, responsavel=?, contato=?
                    WHERE id=?
                ''', (nome, idade, raca, descricao, responsavel, contato, pet_id))

            conn.commit()
            return redirect('/listar')

        # Modo GET: busca dados do pet
        cursor.execute('SELECT * FROM pets WHERE id=?', (pet_id,))
        pet = cursor.fetchone()

    return render_template('editar.html', pet=pet)


# Rota para adotar um pet
@app.route('/adotar/<int:pet_id>', methods=['GET', 'POST'])
def adotar(pet_id):
    with sqlite3.connect('pets.db') as conn:
        cursor = conn.cursor()

        # Busca o pet
        cursor.execute('SELECT * FROM pets WHERE id = ?', (pet_id,))
        pet = cursor.fetchone()

        if not pet:
            return "Pet não encontrado.", 404

        if request.method == 'POST':
            nome_adotante = request.form['nome_adotante']
            email = request.form['email']
            telefone = request.form['telefone']
            mensagem = request.form['mensagem']
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Salvar dados da adoção
            cursor.execute('''
                INSERT INTO adocoes (pet_id, nome_adotante, email, telefone, mensagem, data_adocao)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (pet_id, nome_adotante, email, telefone, mensagem, data))

            # Atualizar status do pet
            cursor.execute('''
                UPDATE pets SET adotado = 1, data_adocao = ? WHERE id = ?
            ''', (data, pet_id))
            conn.commit()

            return redirect('/listar')

        # ✅ Trata valores None antes de enviar ao HTML
        pet = list(pet)
        pet[7] = pet[7] or ""  # campo contato
        pet[6] = pet[6] or ""  # campo responsável (se quiser garantir também)

    return render_template('form_adocao.html', pet=pet)


# Rota para confirmar a adoção
@app.route('/confirmar_adocao/<int:pet_id>', methods=['GET'])
def confirmar_adocao(pet_id):
    with sqlite3.connect('pets.db') as conn:
        cursor = conn.cursor()
        
        # Buscar dados do pet
        cursor.execute('SELECT * FROM pets WHERE id = ?', (pet_id,))
        pet = cursor.fetchone()

        # Buscar dados do adotante e da adoção
        cursor.execute('SELECT * FROM adocoes WHERE pet_id = ?', (pet_id,))
        adotante = cursor.fetchone()

    return render_template('confirmar_adocao.html', pet=pet, adotante=adotante)

# Rota para finalizar a adoção
@app.route('/finalizar_adocao/<int:pet_id>', methods=['POST'])
def finalizar_adocao(pet_id):
    data_adocao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formata a data

    with sqlite3.connect('pets.db') as conn:
        cursor = conn.cursor()
        # Atualiza o status do pet para "adotado" e registra a data de adoção
        cursor.execute('''
            UPDATE pets SET adotado = 1, data_adocao = ? WHERE id = ?
        ''', (data_adocao, pet_id))
        conn.commit()

    return redirect('/listar')  # Redireciona para a lista de pets


# Rota para listar pets
@app.route('/listar')
def listar():
    with sqlite3.connect('pets.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pets')
        pets = cursor.fetchall()

    return render_template('listar.html', pets=pets)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')


print('testecommit')
print('testecommit')
