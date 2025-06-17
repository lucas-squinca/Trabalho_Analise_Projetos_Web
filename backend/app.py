import os
import time
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

# Inicializa a aplicação Flask
app = Flask(__name__)
# Habilita o CORS para permitir que o frontend acesse a API
CORS(app)

def get_db_connection():
    """Estabelece conexão com o banco de dados PostgreSQL."""
    # O loop de retentativa é crucial em ambientes de container,
    # pois o backend pode iniciar antes do banco de dados estar pronto.
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
            print("Conexão com o banco de dados bem-sucedida!")
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            print(f"Não foi possível conectar ao banco. Tentando novamente em 5 segundos... ({retries} tentativas restantes)")
            time.sleep(5)
    # Se todas as tentativas falharem, lança uma exceção.
    raise Exception("Não foi possível conectar ao banco de dados após várias tentativas.")

def init_db():
    """Cria a tabela de tarefas se ela ainda não existir."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Executa o comando SQL para criar a tabela
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            descricao VARCHAR(255) NOT NULL,
            concluida BOOLEAN NOT NULL DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Tabela 'tarefas' inicializada com sucesso.")

# --- Endpoints da API RESTful ---

# Endpoint 1: Obter todas as tarefas (GET /tarefas)
@app.route('/tarefas', methods=['GET'])
def get_tarefas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, descricao, concluida FROM tarefas ORDER BY id ASC;')
    tarefas_db = cur.fetchall()
    cur.close()
    conn.close()

    # Formata a saída como uma lista de dicionários (JSON)
    tarefas = [{'id': row[0], 'descricao': row[1], 'concluida': row[2]} for row in tarefas_db]
    return jsonify(tarefas)

# Endpoint 2: Adicionar uma nova tarefa (POST /tarefas)
@app.route('/tarefas', methods=['POST'])
def add_tarefa():
    dados = request.get_json()
    if not dados or 'descricao' not in dados:
        return jsonify({'erro': 'A descrição da tarefa é obrigatória'}), 400

    descricao = dados['descricao']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tarefas (descricao) VALUES (%s) RETURNING id, descricao, concluida;', (descricao,))
    nova_tarefa = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    tarefa_criada = {'id': nova_tarefa[0], 'descricao': nova_tarefa[1], 'concluida': nova_tarefa[2]}
    return jsonify(tarefa_criada), 201

# Endpoint 3: Atualizar uma tarefa (marcar como concluída/pendente) (PUT /tarefas/<id>)
@app.route('/tarefas/<int:id>', methods=['PUT'])
def update_tarefa(id):
    dados = request.get_json()
    if 'concluida' not in dados or not isinstance(dados['concluida'], bool):
        return jsonify({'erro': 'O campo "concluida" (booleano) é obrigatório'}), 400
    
    concluida = dados['concluida']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tarefas SET concluida = %s WHERE id = %s;', (concluida, id))
    conn.commit()
    
    # Verifica se alguma linha foi realmente atualizada
    updated_rows = cur.rowcount
    cur.close()
    conn.close()

    if updated_rows == 0:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
        
    return jsonify({'sucesso': True, 'mensagem': f'Tarefa {id} atualizada.'})

if __name__ == '__main__':
    # Garante que a tabela exista antes de iniciar a aplicação
    init_db()
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000)
