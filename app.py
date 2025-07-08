from flask import Flask, request, jsonify
import openai
import os
from datetime import datetime

# Iniciar app Flask
app = Flask(__name__)

# Definir a chave da OpenAI (use variável de ambiente no Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Página inicial
@app.route('/')
def home():
    return '''
    🤖 Dany AI - Webhook Ativo!
    ✅ Sistema funcionando com OpenAI
    🕐 Status: ONLINE
    '''

# Status
@app.route('/status')
def status():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'modelo': 'gpt-3.5-turbo'
    })

# Rota para testar a resposta da Dany via POST
@app.route('/dany', methods=['POST'])
def responder():
    dados = request.get_json()
    pergunta = dados.get("mensagem", "")

    if not pergunta:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = gerar_resposta_dany(pergunta)
    return jsonify({"resposta": resposta})

# Função que chama a API da OpenAI
def gerar_resposta_dany(pergunta):
    try:
        resposta = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é Dany, uma consultora de emagrecimento atenciosa e alegre."},
        {"role": "user", "content": pergunta}
    ]
)
(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é Dany, uma consultora de emagrecimento atenciosa e alegre."},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"


# Rodar localmente
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


