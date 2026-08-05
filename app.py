import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///apostas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Aposta(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  evento = db.Column(db.String(100), nullable=False)
  estrategia = db.Column(db.String(50), nullable=False)
  investimento = db.Column(db.Float, nullable=False)
  status = db.Column(db.String(20), default="Pendente")


with app.app_context():
  db.create_all()


# Rota Principal agora é a Calculadora
@app.route("/")
def index():
  return render_template("index.html")


# Rota do Dashboard / Histórico separada
@app.route("/dashboard")
def dashboard():
  apostas = Aposta.query.all()
  investimento_total = sum(a.investimento for a in apostas if a.investimento)
  lucro_total = 0.0
  roi_acumulado = (
      (lucro_total / investimento_total) * 100 if investimento_total > 0 else 0.0
  )

  return render_template(
      "dashboard.html",
      apostas=apostas,
      lucro_total=lucro_total,
      investimento_total=investimento_total,
      roi_acumulado=roi_acumulado,
  )


@app.route("/painel_bonus")
def painel_bonus():
  return render_template("painel_bonus.html")


@app.route("/nova", methods=["POST", "GET"])
def nova_aposta():
  if request.method == "POST":
    evento = request.form.get("evento", "Evento Desconhecido")
    estrategia = request.form.get("estrategia", "Sistema de Arbitragem")
    valores = request.form.getlist("valor")
    investimento_total = sum(
        float(v.replace(",", ".")) for v in valores if v.replace(".", "").isdigit()
    )

    nova = Aposta(
        evento=evento,
        estrategia=estrategia,
        investimento=investimento_total,
        status="Pendente",
    )
    db.session.add(nova)
    db.session.commit()
    return redirect(url_for("dashboard"))

  return redirect(url_for("index"))


@app.route("/excluir/<int:id>")
def excluir_aposta(id):
  aposta = Aposta.query.get_or_404(id)
  db.session.delete(aposta)
  db.session.commit()
  return redirect(url_for("dashboard"))


if __name__ == "__main__":
  app.run(debug=True)
