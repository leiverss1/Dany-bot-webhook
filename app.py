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
    usuario = dados.get("usuario", "")

    if not pergunta:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = gerar_resposta_dany(pergunta, usuario)
    return jsonify({"resposta": resposta})

def gerar_resposta_dany(pergunta, usuario):
    try:
        pergunta_lower = pergunta.lower()

        # Resposta direta para dúvidas sobre onde comprar
        if "comprar" in pergunta_lower or "site" in pergunta_lower or "adquirir" in pergunta_lower:
            return (
                "Você pode adquirir nossos produtos diretamente pelos links abaixo:\n\n"
                "🟢 SB2 Turbo: https://mmecoserv.com/sb2turbo\n"
                "⚫ SB2 Black: https://mmecoserv.com/sb2black\n\n"
                "Esses são os sites oficiais, com garantia de qualidade e entrega segura. "
                "Se precisar de ajuda durante o processo de compra, estou aqui pra te ajudar, amiga! 💪😊"
            )

        # Prompt com personalização
        mensagens = [
            {"role": "system", "content": (
                f"Você é Dany, uma consultora de emagrecimento simpática, acolhedora e vendedora.\n"
                f"Seu objetivo é ajudar mulheres a conquistarem autoestima e saúde com os produtos SB2 Turbo e SB2 Black.\n"
                f"Quando souber o nome da cliente, use com carinho.\n"
                f"Quando ela disser que quer emagrecer, perder barriga, controlar o apetite ou algo parecido, reconheça isso como a dor principal dela e trate com empatia.\n"
                f"Você pode dar dicas rápidas de emagrecimento para gerar valor, mas sempre volte a apresentar os produtos como solução.\n"
                f"Finalize as conversas com leveza e encorajamento."
            )},
            {"role": "user", "content": pergunta}
        ]

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



