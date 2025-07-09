from flask import Flask, request, jsonify
import openai
import os
import re
from datetime import datetime

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return '''
    🤖 Dany AI - Webhook Ativo!
    ✅ Sistema funcionando com OpenAI
    🕐 Status: ONLINE
    '''

@app.route('/status')
def status():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'modelo': 'gpt-3.5-turbo'
    })

@app.route('/dany', methods=['POST'])
def responder():
    dados = request.get_json()
    pergunta = dados.get("mensagem", "")
    usuario = dados.get("usuario", "")

    if not pergunta:
        return jsonify({"erro": "Mensagem vazia"}), 400

    nome = extrair_nome(pergunta)
    cidade = extrair_cidade(pergunta)
    dor = detectar_dor(pergunta)

    resposta = gerar_resposta_dany(pergunta, nome, cidade, dor)
    return jsonify({"resposta": resposta})

def extrair_nome(mensagem):
    padrao = re.search(r"(?i)me chamo ([A-Za-zÀ-ÿ]+)|sou a ([A-Za-zÀ-ÿ]+)|aqui é a ([A-Za-zÀ-ÿ]+)", mensagem)
    if padrao:
        grupos = padrao.groups()
        return next((g for g in grupos if g), None)
    return None

def extrair_cidade(mensagem):
    padrao = re.search(r"(?i)em ([A-Za-zÀ-ÿ\s]+)|de ([A-Za-zÀ-ÿ\s]+)", mensagem)
    if padrao:
        grupos = padrao.groups()
        return next((g.strip() for g in grupos if g), None)
    return None

def detectar_dor(mensagem):
    if re.search(r"(?i)emagrecer|perder peso", mensagem):
        return "emagrecer"
    elif re.search(r"(?i)barriga|abdômen", mensagem):
        return "reduzir barriga"
    elif re.search(r"(?i)apetite|fome|compulsão", mensagem):
        return "controlar o apetite"
    return None

def gerar_resposta_dany(pergunta, nome=None, cidade=None, dor=None):
    try:
        mensagens = []

        system_msg = "Você é Dany, uma consultora de emagrecimento simpática, acolhedora e divertida. Seu papel é vender os produtos SB2 Turbo e SB2 Black, oferecendo respostas personalizadas, mencionando o nome da cliente se disponível, reconhecendo cidades citadas, e utilizando emojis e linguagem leve. Ao final de cada compra ou dúvida respondida, incentive com simpatia e esteja disponível para ajudar mais."
        mensagens.append({"role": "system", "content": system_msg})

        prompt_usuario = pergunta
        contexto = []

        if nome:
            contexto.append(f"O nome da cliente é {nome}.")
        if cidade:
            contexto.append(f"Ela é da cidade de {cidade}.")
        if dor:
            contexto.append(f"Ela mencionou a dor principal: {dor}.")

        if contexto:
            prompt_usuario = "\n".join(contexto) + "\n" + pergunta

        mensagens.append({"role": "user", "content": prompt_usuario})

        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensagens
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERRO] Falha na geração de resposta: {str(e)}")
        return "❌ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



