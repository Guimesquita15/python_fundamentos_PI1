from flask import Flask, render_template, request
import os  # Importe o módulo os aqui

app = Flask(_name_)

def img_exists(img_path):
    return os.path.exists(os.path.join(app.static_folder, img_path))

# Restante do código...
    

# Adicionar a função img_exists ao contexto do Jinja2
app.jinja_env.globals['img_exists'] = img_exists

class Filme:
    def _init_(self, titulo, descricao, horarios):
        self.titulo = titulo
        self.descricao = descricao
        self.horarios = horarios

class Sala:
    def _init_(self, numero, filas, assentos_por_fila):
        self.numero = numero
        self.filas = filas
        self.assentos_por_fila = assentos_por_fila
        self.assentos = {fila: [False] * assentos_por_fila for fila in filas}

    def escolher_assento(self, fila, assento):
        if not self.assentos[fila][assento]:
            self.assentos[fila][assento] = True
            return True
        return False

class Cinema:
    def _init_(self):
        self.filmes = []
        self.salas = {}
        self.pacotes = {
            'pequeno': 6.20,
            'grande': 8.40,
            'estudante': 6.50
        }

    def adicionar_filme(self, filme, sala):
        self.filmes.append(filme)
        self.salas[filme.titulo] = sala

    def escolher_filme(self, titulo):
        for filme in self.filmes:
            if filme.titulo == titulo:
                return filme
        return None

    def obter_preco_pacote(self, tipo_pacote):
        return self.pacotes.get(tipo_pacote, 0.0)



cinema = Cinema()
cinema.adicionar_filme(Filme("O Exterminador Implacável", "Ação/Ficção científica", ["18:00", "20:00", "23:30"]), Sala(1, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], 14))
cinema.adicionar_filme(Filme("Titanic", "Romance/Drama", ["12:00","15:00", "20:00"]), Sala(2, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], 14))
cinema.adicionar_filme(Filme("O Rei Leão", "Animação/Aventura", ["09:45", "14:30", "16:00"]), Sala(3, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], 14))
cinema.adicionar_filme(Filme("Homem-Aranha", "Ação/Aventura", ["13:30", "17:40", "21:00"]), Sala(4, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], 14))

@app.route('/' )
def index():
    filmes = cinema.filmes
    horarios_por_filme = {filme.titulo: filme.horarios for filme in filmes}
    return render_template('index.html', filmes=filmes, horarios_por_filme=horarios_por_filme)

@app.route('/escolher_assento', methods=['POST'])
def escolher_assento():
    # Seu código para a função escolher_assento...
    if preco_pacote > 0.0:
        preco_total = 10.0 + preco_pacote  # Preço base do ingresso
        mensagem = f"Assento reservado com sucesso! Boa sessão! Preço total: {preco_total:.2f}€"
        return render_template('bilhete.html', filmes=titulo_filme, horario=horario) 


if _name_ == '_main_':
    app.run(debug=True)