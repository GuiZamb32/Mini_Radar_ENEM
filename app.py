import logging
import os

from flask import Flask, jsonify, request


def setting(name, default):
    """Read non-secret runtime configuration from the environment."""
    return os.getenv(name, default)


AMBIENTE = setting("AMBIENTE", "desenvolvimento")
INSTANCIA_NOME = setting("INSTANCIA_NOME", "radar-local")
VERSAO = setting("APP_VERSION", "v3")
PORTA = int(setting("PORT", "5000"))

logging.basicConfig(
    level=setting("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("radar_enem")

app = Flask(__name__)


@app.after_request
def registrar_resposta(response):
    logger.info("method=%s path=%s status=%s", request.method, request.path, response.status_code)
    return response


@app.route("/")
def home():
    return jsonify(
        {
            "projeto": "Radar ENEM",
            "disciplina": "Computacao em Nuvem",
            "status": "online",
            "ambiente": AMBIENTE,
            "instancia": INSTANCIA_NOME,
            "versao": VERSAO,
        }
    )


@app.route("/health")
def health():
    """Endpoint sem autenticação para orquestrador e monitoramento local."""
    return jsonify({"status": "healthy", "versao": VERSAO, "ambiente": AMBIENTE}), 200


@app.route("/aluno/<nome>")
def aluno(nome):
    return jsonify(
        {
            "aluno": nome,
            "ambiente": AMBIENTE,
            "mensagem": "Bem-vindo ao Mini Radar ENEM",
        }
    )


@app.route("/nota/<int:nota>")
def consultar_nota(nota):
    classificacao = "acima de 600" if nota >= 600 else "abaixo de 600"
    return jsonify({"nota": nota, "classificacao": classificacao})


@app.route("/estatisticas")
def estatisticas():
    return jsonify(
        {
            "total_consultas_simuladas": 1250,
            "media_corte_geral": 680.5,
            "status_metrica": "ok",
        }
    )


if __name__ == "__main__":
    logger.info("iniciando ambiente=%s instancia=%s versao=%s", AMBIENTE, INSTANCIA_NOME, VERSAO)
    app.run(host="0.0.0.0", port=PORTA)
