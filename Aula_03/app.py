from flask import Flask, jsonify
import os

app = Flask(__name__)

# Configurações por variáveis de ambiente (Desafio Extra)
AMBIENTE = os.getenv("AMBIENTE", "desenvolvimento")
INSTANCIA_NOME = os.getenv("INSTANCIA_NOME", "Radar-Local")

@app.route("/")
def home():
    return jsonify({
        "projeto": "Radar ENEM",
        "disciplina": "Computacao em Nuvem",
        "status": "online",
        "instancia": INSTANCIA_NOME
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/aluno/<nome>")
def aluno(nome):
    return jsonify({
        "aluno": nome,
        "ambiente": AMBIENTE,
        "mensagem": "Bem-vindo ao Mini Radar ENEM"
    })

# Endpoint do Desafio v2
@app.route("/nota/<int:nota>")
def consultar_nota(nota):
    classificacao = "acima de 600" if nota >= 600 else "abaixo de 600"
    return jsonify({
        "nota": nota,
        "classificacao": classificacao
    })

# Novo Endpoint Personalizado (Desafio Extra)
@app.route("/estatisticas")
def estatisticas():
    return jsonify({
        "total_consultas_simuladas": 1250,
        "media_corte_geral": 680.5,
        "status_metrica": "ok"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)