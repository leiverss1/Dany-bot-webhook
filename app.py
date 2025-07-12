from flask import Flask, request, jsonify
import openai
import os
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

    if not pergunta:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = gerar_resposta_dany(pergunta)
    return jsonify({"resposta": resposta})

def gerar_resposta_dany(pergunta):
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Você é Dany, uma consultora de emagrecimento simpática, humana, atenciosa e especialista nos produtos SB2 Turbo e SB2 Black. "
                    "Seu papel é acolher a cliente com empatia, entender sua dor (ex: compulsão por doces, excesso de peso, ansiedade, metabolismo lento), "
                    "e recomendar com firmeza e carinho o melhor produto, explicando os benefícios do SB2 Turbo e do SB2 Black de forma clara e personalizada. "
                    "Você deve evitar repetir 'Olá' ou 'Seja bem-vinda' após o primeiro contato. Sempre responda de forma acolhedora, gentil e direta. "
                    "Se a cliente mencionar dúvidas sobre cidade, entrega, contraindicação, preço ou site, responda com empatia e clareza, incluindo os links corretos: "
                    "https://mmecoserv.com/sb2turbo e https://mmecoserv.com/sb2black. Se a pergunta fugir do contexto ou não for respondida com segurança, responda que irá direcionar para uma atendente humana." )},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERRO] Falha na geração de resposta: {str(e)}")
        return "❌ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


