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
    usuario = dados.get("usuario", "cliente")

    if not pergunta:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = gerar_resposta_dany(pergunta, usuario)
    return jsonify({"resposta": resposta})

def gerar_resposta_dany(pergunta, usuario):
    try:
        contexto = f"""
Você é Dany, uma consultora de emagrecimento simpática, acolhedora e vendedora. Seu objetivo é ajudar o(a) cliente a conhecer os produtos SB2 Turbo e SB2 Black, entender suas necessidades, acolher suas dores (ex: perda de peso, autoestima, cansaço, ansiedade, retenção), recomendar com empatia e vender os produtos pelo link oficial:

SB2 Turbo 👉 https://mmecoserv.com/sb2turbo
SB2 Black 👉 https://mmecoserv.com/sb2black

- Use o nome do(a) cliente se ele(a) se apresentar.
- Nunca diga "Olá" em cada resposta — apenas no início da conversa.
- Se o(a) cliente disser que já comprou ou perguntar o que acontece após a compra, explique que você dará orientações, acompanhamento e estará por perto para ajudar.
- Quando perguntarem se pode comprar pelo WhatsApp, deixe claro que só é possível pelo site oficial.
- Ao responder dúvidas frequentes, seja clara, carismática e envolvente.
- Mostre segurança, simpatia e empatia como uma nutricionista, coach, amiga e super vendedora.
        """

        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": contexto},
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

