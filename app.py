from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

def img_exists(img_path):
    return os.path.exists(os.path.join(app.static_folder, img_path))

app.jinja_env.globals['img_exists'] = img_exists

class Filme:
    def __init__(self, titulo, descricao, horarios):
        self.titulo = titulo
        self.descricao = descricao
        self.horarios = horarios

class Sala:
    def __init__(self, numero, filas, assentos_por_fila):
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
    def __init__(self):
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
cinema.adicionar_filme(Filme("O Exterminador Implacável", "Ação/Ficção científica", ["18:00", "20:00", "23:30"]), Sala(1, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], 18))
cinema.adicionar_filme(Filme("Titanic", "Romance/Drama", ["12:00", "15:00", "20:00"]), Sala(2, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], 18))
cinema.adicionar_filme(Filme("O Rei Leão", "Animação/Aventura", ["09:45", "14:30", "16:00"]), Sala(3, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], 18))
cinema.adicionar_filme(Filme("Homem-Aranha", "Ação/Aventura", ["13:30", "17:40", "21:00"]), Sala(4, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], 18))

@app.route('/')
def index():
    filmes = cinema.filmes
    horarios_por_filme = {filme.titulo: filme.horarios for filme in filmes}
    return render_template('index.html', filmes=filmes, horarios_por_filme=horarios_por_filme)

@app.route('/escolher_assento', methods=['POST'])
def escolher_assento():
    titulo_filme = request.form.get('titulo_filme')
    horario = request.form.get('horario')
    fila = request.form.get('fila')
    assento = int(request.form.get('assento'))
    tipo_pacote = request.form.get('tipo_pacote')

    print(f"Filme: {titulo_filme}, Horário: {horario}, Fila: {fila}, Assento: {assento}, Pacote: {tipo_pacote}")

    filme = cinema.escolher_filme(titulo_filme)
    if filme:
        sala = cinema.salas[filme.titulo]
        if sala.escolher_assento(fila, assento):
            preco_pacote = cinema.obter_preco_pacote(tipo_pacote)
            preco_total = 10.0 + preco_pacote  # Preço base do ingresso
            mensagem = f"Assento reservado com sucesso!  Preço total: {preco_total:.2f}€ Boa sessão!"
            return render_template('bilhete.html', titulo_filme=titulo_filme, horario=horario, mensagem=mensagem)
        else:
            return "Assento indisponivel ou ocupado. Por favor, escolha outro assento."
    return "Falha na reserva do assento. Tente novamente."

if __name__ == '__main__':
    app.run(debug=True)
