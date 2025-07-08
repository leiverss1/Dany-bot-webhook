from flask import Flask, request, jsonify
import openai
import os
from datetime import datetime

app = Flask(__name__)

# Configure a chave da OpenAI via variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Página inicial
@app.route('/')
def home():
    return '''
    🤖 Dany AI - Webhook Ativo!<br>
    ✅ Sistema funcionando com OpenAI<br>
    🕐 Status: ONLINE
    '''

# Endpoint de status
@app.route('/status')
def status():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'modelo': 'gpt-3.5-turbo'
    })

# Endpoint principal para o Venom enviar mensagens
@app.route('/dany', methods=['POST'])
def responder():
    dados = request.get_json()
    mensagem = dados.get("mensagem", "")
    usuario = dados.get("usuario", "")

    if not mensagem:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = gerar_resposta_dany(mensagem, usuario)
    return jsonify({"resposta": resposta})


def gerar_resposta_dany(pergunta, usuario):
    try:
        # Funil de vendas básico com gatilhos
        pergunta_lower = pergunta.lower()

        if any(saud in pergunta_lower for saud in ["oi", "olá", "boa tarde", "bom dia", "boa noite"]):
            return f"Oi! Seja bem-vindo(a). Eu sou a Dany 🤖, sua consultora de emagrecimento. Posso te ajudar a conhecer nossos produtos SB2 Turbo e SB2 Black. Qual seu objetivo hoje?"

        if "sb2 turbo" in pergunta_lower:
            return "O SB2 Turbo é perfeito para quem busca acelerar o metabolismo e emagrecer com mais energia! 💥 Veja mais aqui: https://mmecoserv.com/sb2turbo"

        if "sb2 black" in pergunta_lower:
            return "O SB2 Black é ideal para controle de apetite e queima de gordura localizada! 🔥 Confira: https://mmecoserv.com/sb2black"

        if "quero comprar" in pergunta_lower or "como comprar" in pergunta_lower:
            return "Você pode comprar diretamente pelos links abaixo:\n👉 SB2 Turbo: https://mmecoserv.com/sb2turbo\n👉 SB2 Black: https://mmecoserv.com/sb2black\nSe tiver dúvidas, posso te ajudar!"

        # Caso contrário, usa a IA da OpenAI
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é Dany, uma consultora de emagrecimento atenciosa e alegre. Responda com simpatia e clareza, como uma vendedora experiente."},
                {"role": "user", "content": pergunta}
            ]
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERRO] Falha na geração de resposta: {str(e)}")
        return "❌ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."


# Rodar localmente ou no Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




