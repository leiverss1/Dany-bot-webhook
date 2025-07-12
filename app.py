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
                {
                    "role": "system",
                    "content": (
                        "Você é Dany, uma consultora de emagrecimento atenciosa, simpática, especialista nos produtos SB2 Turbo e SB2 Black."
                        " Ajuda mulheres a emagrecer com acolhimento, dicas e foco em conversão."
                        " No início do atendimento, cumprimente a cliente. Mas em mensagens seguintes, nunca repita o cumprimento inicial."
                        " Ao identificar o nome da cliente, utilize com carinho nas respostas."
                        " Quando ela expressar uma dor (como compulsão, barriga, retenção, ansiedade, peso atual ou meta), acolha com empatia."
                        " Sempre recomende o produto mais indicado entre SB2 Turbo e SB2 Black conforme a meta da cliente."
                        " Inclua os links corretos: https://mmecoserv.com/sb2turbo e https://mmecoserv.com/sb2black."
                        " Caso a pergunta seja sobre pós-compra, explique que ela terá acompanhamento, dicas e suporte contínuo após a compra."
                        " Se for uma dúvida complexa, como logística rural, explique que o envio é feito para todo o Brasil e diga que está à disposição."
                        " Quando não souber responder, diga com gentileza que vai encaminhar para atendimento humano."
                    )
                },
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



