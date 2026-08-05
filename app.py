import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///apostas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Modelo do Banco de Dados
class Aposta(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  titulo = db.Column(db.String(100), nullable=False)
  casa = db.Column(db.String(50), nullable=False)
  valor = db.Column(db.Float, nullable=False)
  odd = db.Column(db.Float, nullable=False)
  status = db.Column(db.String(20), default="Pendente")


with app.app_context():
  db.create_all()


# Rota Principal (Página Inicial)
@app.route("/")
def index():
  apostas = Aposta.query.all()
  return render_template("index.html", apostas=apostas)


# Rota para Adicionar Nova Aposta
@app.route("/nova", methods=["GET", "POST"])
def nova_aposta():
  if request.method == "POST":
    titulo = request.form["titulo"]
    casa = request.form["casa"]
    valor = float(request.form["valor"])
    odd = float(request.form["odd"])

    nova = Aposta(titulo=titulo, casa=casa, valor=valor, odd=odd)
    db.session.add(nova)
    db.session.commit()
    return redirect(url_for("index"))

  return render_template("nova_aposta.html")


# Rota para Editar Aposta
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_aposta(id):
  aposta = Aposta.query.get_or_404(id)
  if request.method == "POST":
    aposta.titulo = request.form["titulo"]
    aposta.casa = request.form["casa"]
    aposta.valor = float(request.form["valor"])
    aposta.odd = float(request.form["odd"])
    aposta.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("index"))

  return render_template("editar_aposta.html", aposta=aposta)


# Rota para Excluir Aposta
@app.route("/excluir/<int:id>")
def excluir_aposta(id):
  aposta = Aposta.query.get_or_404(id)
  db.session.delete(aposta)
  db.session.commit()
  return redirect(url_for("index"))


# Rota para Painel de Bônus
@app.route("/bonus")
def painel_bonus():
  return render_template("painel_bonus.html")


if __name__ == "__main__":
  app.run(debug=True)