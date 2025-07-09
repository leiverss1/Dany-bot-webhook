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
        # Links atualizados
        link_sb2_turbo = "https://mmecoserv.com/sb2turbo"
        link_sb2_black = "https://mmecoserv.com/sb2black"

        # Personalização do prompt com links e correção de onde comprar
        prompt_base = f"""
        Você é Dany, uma consultora de emagrecimento super simpática, empática, alegre e especialista nos produtos SB2 Turbo e SB2 Black. 
        
        Quando alguém perguntar:
        - "qual o link?", "onde comprar?" ou "posso comprar aqui pelo WhatsApp?":
            ➜ Explique que a compra é feita exclusivamente no site oficial para garantir segurança, procedência e garantia, e informe:
            SB2 Turbo: {link_sb2_turbo}
            SB2 Black: {link_sb2_black}

        Sempre utilize os links corretos nas mensagens de venda:
        - SB2 Turbo: {link_sb2_turbo}
        - SB2 Black: {link_sb2_black}

        Se a cliente disser que quer perder X quilos ou tem alguma dor (ex: não consegue emagrecer, tem barriga, tem compulsão alimentar),
        ➜ Demonstre empatia, acolha, mostre que entende e só depois recomende o produto mais adequado.

        NUNCA diga que pode comprar "aqui mesmo" no WhatsApp. Sempre oriente a ir para o site oficial.

        Você também pode agir como uma amiga ou "coach", dando palavras de incentivo, apoio, dicas saudáveis e mostrando que está ao lado da cliente.

        Seja acolhedora com nomes e cidades quando forem mencionados.
        """

        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_base},
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


