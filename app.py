from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
db = SQLAlchemy(app)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    data_nascimento = db.Column(db.Date)

# Rota principal
@app.route("/")
def index():
    contatos = Contato.query.order_by(Contato.nome).all()
    return render_template("index.html", contatos=contatos)

# Rota para adicionar um novo contato
@app.route("/adicionar_contato", methods=["POST"])
def adicionar_contato():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        endereco = request.form["endereco"]
        data_nascimento = request.form["data_nascimento"]

        novo_contato = Contato(nome=nome, email=email, telefone=telefone, endereco=endereco, data_nascimento=data_nascimento)
        db.session.add(novo_contato)
        db.session.commit()

        return redirect(url_for("index"))

# Rota para editar um contato
@app.route("/editar_contato/<int:id>", methods=["GET", "POST"])
def editar_contato(id):
    contato = Contato.query.get(id)

    if request.method == "POST":
        contato.nome = request.form["nome"]
        contato.email = request.form["email"]
        contato.telefone = request.form["telefone"]
        contato.endereco = request.form["endereco"]
        contato.data_nascimento = request.form["data_nascimento"]

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("editar_contato.html", contato=contato)

# Rota para excluir um contato
@app.route("/excluir_contato/<int:id>")
def excluir_contato(id):
    contato = Contato.query.get(id)
    db.session.delete(contato)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

