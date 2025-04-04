from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import random
import os

app = Flask(__name__)
CORS(app)

REMETENTE = "ferreiramateuss000@gmail.com"
SENHA_APP = "yvsdhnqamzqkhmay"  # Senha de app gerada no Gmail

def enviar_email(email_cliente, senha):
    mensagem = f"""\ 
Assunto: Acesso à Plataforma

Olá! Obrigado pela compra. Aqui estão seus dados de acesso:

🌐 Plataforma: https://seudominio.com
📧 E-mail: {email_cliente}
🔑 Senha: {senha}
"""

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(REMETENTE, SENHA_APP)
            server.sendmail(REMETENTE, email_cliente, mensagem.encode("utf-8"))
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

@app.route("/")
def home():
    return "🟢 API da Plataforma está online!"

@app.route("/webhook_kirvano", methods=["POST"])
def webhook_kirvano():
    dados = request.get_json()
    
    # Log para ver o que a Kirvano está enviando
    print("🔍 Dados recebidos da Kirvano:", dados)

    # Verifica se os dados chegaram corretamente
    if not dados:
        return jsonify({"erro": "Nenhum dado recebido"}), 400

    # Tenta pegar o e-mail de diferentes formas
    email_cliente = dados.get("cliente_email") or dados.get("email") or dados.get("user_email")
    status = dados.get("status")

    # Verifica se os dados são válidos
    if status == "aprovado" and email_cliente:
        senha_gerada = str(random.randint(10000, 99999))
        sucesso = enviar_email(email_cliente, senha_gerada)

        if sucesso:
            return jsonify({"mensagem": "E-mail enviado com sucesso!", "email": email_cliente, "senha": senha_gerada}), 200
        else:
            return jsonify({"erro": "Erro ao enviar o e-mail"}), 500
    else:
        return jsonify({"erro": "Compra não aprovada ou dados incompletos"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
