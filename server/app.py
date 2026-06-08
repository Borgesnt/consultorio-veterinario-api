from flask import Flask, request, jsonify, render_template

from models import Animal, Consulta
from mq.producer import publish_message
from utils.database import carregar

app = Flask(__name__)


@app.route("/")
def home():
    return {
        "status": "online",
        "service": "Clinica Veterinaria API"
    }


@app.route("/animais", methods=["POST"])
def cadastrar_animal():

    dados = request.json

    publish_message({
        "acao": "cadastrar_animal",
        "dados": dados
    })

    return jsonify({
        "status": "Mensagem enviada para fila"
    })


@app.route("/animais", methods=["GET"])
def listar_animais():

    db = carregar()

    return jsonify(
        db["animais"]
    )


@app.route("/consultas", methods=["POST"])
def registrar_consulta():

    dados = request.json

    publish_message({
        "acao": "registrar_consulta",
        "dados": dados
    })

    return jsonify({
        "status": "Consulta enviada para fila"
    })


@app.route("/consultas", methods=["GET"])
def listar_consultas():

    db = carregar()

    return jsonify(
        db["consultas"]
    )


@app.route("/api/stats")
def stats():

    db = carregar()

    return {
        "animais": len(db["animais"]),
        "consultas": len(db["consultas"]),
        "mensagens": db["mensagens_processadas"]
    }


@app.route("/dashboard")
def dashboard():

    db = carregar()

    return render_template(
        "dashboard.html",
        animais=db["animais"],
        consultas=db["consultas"],
        mensagens=db["mensagens_processadas"],
        eventos=db["eventos"]
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )