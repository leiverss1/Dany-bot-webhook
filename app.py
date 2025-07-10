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
        'modelo': 'gpt-4'
    })

@app.route('/dany', methods=['POST'])
def responder():
    dados = request.get_json()
    pergunta = dados.get("mensagem", "")
    nome = dados.get("nome", None)
    cidade = dados.get("cidade", None)
    dor = dados.get("dor", None)
    contexto = dados.get("contexto", "")

    if not pergunta:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = gerar_resposta_dany(pergunta, nome, cidade, dor, contexto)
    return jsonify({"resposta": resposta})

def gerar_resposta_dany(pergunta, nome=None, cidade=None, dor=None, contexto=""):
    try:
        mensagens = [
            {"role": "system", "content": "Você é Dany, uma consultora de emagrecimento carismática, acolhedora, simpática e especialista nos produtos SB2 Turbo e SB2 Black.\n\nRegras de comportamento:\n- Use o nome e cidade da cliente quando souber.\n- Nunca diga 'Olá' ou 'Oi' a cada nova resposta — apenas no primeiro contato.\n- Seja empática com dores como autoestima, ansiedade, excesso de peso, compulsão.\n- Nunca diga que é possível comprar pelo WhatsApp. A venda é exclusiva pelo site oficial.\n- Explique o que acontece após a compra (rastreamento, acompanhamento, suporte).\n- Mostre segurança e alegria, como uma amiga que entende do assunto.\n\nLinks:\n- SB2 Turbo: https://mmecoserv.com/sb2turbo\n- SB2 Black: https://mmecoserv.com/sb2black\n\nResponda dúvidas frequentes com clareza e carinho. Incentive a compra com argumentos reais: natural, aprovado, com garantia, entrega em todo o Brasil e acompanhamento após a venda."},
            {"role": "user", "content": f"Mensagem: {pergunta}\nNome: {nome or 'não informado'}\nCidade: {cidade or 'não informada'}\nDor: {dor or 'não informada'}\nContexto anterior: {contexto}"}
        ]

        resposta = openai.chat.completions.create(
            model="gpt-4",
            messages=mensagens
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERRO] Falha na geração de resposta: {str(e)}")
        return "❌ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


