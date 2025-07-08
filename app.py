from flask import Flask, request, jsonify
import openai
import os
from datetime import datetime

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return 'Dany-bot Webhook ativo!'

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

    resposta = gerar_resposta_dany(pergunta, dados.get("usuario"))
    return jsonify({"resposta": resposta})

# Histórico simples por usuário
usuarios = {}

# Função principal
funil_boas_vindas = """
Você é Dany 🏋️‍♀️, uma consultora de emagrecimento leve, simpática e vendedora. 
Seu objetivo principal é vender os produtos **SB2 Turbo** e **SB2 Black**, explicando os benefícios com entusiasmo e naturalidade. 

Ao conversar com o cliente, siga esse fluxo:

1. Cumprimente de forma amigável apenas no primeiro contato. 
2. Pergunte qual o objetivo da pessoa: emagrecer, ter mais energia, secar barriga?
3. Apresente os produtos SB2 com foco no objetivo informado.
4. Use provas sociais e frases motivadoras. Ex: "Tem gente que perdeu até 4kg na primeira semana!".
5. Envie os links dos produtos no momento certo:
   - SB2 Turbo: https://mmecoserv.com/sb2turbo
   - SB2 Black: https://mmecoserv.com/sb2black
6. Tire dúvidas e feche a venda de forma natural.
7. Após a compra, ofereça acompanhamento com dicas motivacionais e alimentação para fidelizar o cliente.

Seja simpática, divertida e com vibe de "amiga que entende do assunto". Mantenha o foco em conversão, mas sem pressão.
"""

def gerar_resposta_dany(pergunta, usuario=None):
    try:
        contexto_usuario = usuarios.get(usuario, [])
        mensagens = [
            {"role": "system", "content": funil_boas_vindas}
        ] + contexto_usuario[-5:] + [
            {"role": "user", "content": pergunta}
        ]

        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensagens
        )

        texto = resposta.choices[0].message.content.strip()
        contexto_usuario.append({"role": "user", "content": pergunta})
        contexto_usuario.append({"role": "assistant", "content": texto})
        usuarios[usuario] = contexto_usuario[-10:]  # manter um histórico enxuto

        return texto

    except Exception as e:
        print(f"[ERRO] Falha ao gerar resposta: {str(e)}")
        return "⚠️ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


