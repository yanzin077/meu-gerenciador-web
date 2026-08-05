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
  evento = db.Column(db.String(100), nullable=False)
  estrategia = db.Column(db.String(50), nullable=False)
  investimento = db.Column(db.Float, nullable=False)
  status = db.Column(db.String(20), default="Pendente")


with app.app_context():
  db.create_all()


# Rota Principal (Calculadora)
@app.route("/")
def index():
  apostas = Aposta.query.all()

  lucro_total = 0.0
  investimento_total = 0.0

  for a in apostas:
    if a.investimento:
      investimento_total += a.investimento

  roi_acumulado = (
      (lucro_total / investimento_total) * 100 if investimento_total > 0 else 0.0
  )

  return render_template(
      "index.html",
      apostas=apostas,
      lucro_total=lucro_total,
      investimento_total=investimento_total,
      roi_acumulado=roi_acumulado,
  )


# Rota do Painel de Bônus
@app.route("/painel_bonus")
def painel_bonus():
  return render_template("painel_bonus.html")


# Rota para Adicionar Nova Aposta via Calculadora (Aceita POST e GET)
@app.route("/nova", methods=["POST", "GET"])
def nova_aposta():
  if request.method == "POST":
    evento = request.form.get("evento", "Evento Desconhecido")
    estrategia = request.form.get("estrategia", "Sistema de Arbitragem")

    valores = request.form.getlist("valor")
    investimento_total = 0.0
    for v in valores:
      try:
        val_limpo = float(v.replace(",", "."))
        investimento_total += val_limpo
      except ValueError:
        pass

    nova = Aposta(
        evento=evento,
        estrategia=estrategia,
        investimento=investimento_total,
        status="Pendente",
    )
    db.session.add(nova)
    db.session.commit()

  return redirect(url_for("index"))


# Rota para Excluir Aposta
@app.route("/excluir/<int:id>")
def excluir_aposta(id):
  aposta = Aposta.query.get_or_404(id)
  db.session.delete(aposta)
  db.session.commit()
  return redirect(url_for("index"))


if __name__ == "__main__":
  app.run(debug=True)
