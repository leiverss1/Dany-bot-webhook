from flask import Flask, request, jsonify
import openai
import os
from datetime import datetime
import re

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
    usuario = dados.get("usuario", "anonimo")

    if not pergunta:
        return jsonify({"erro": "Mensagem vazia"}), 400

    resposta = gerar_resposta_dany(pergunta, usuario)
    return jsonify({"resposta": resposta})

usuarios = {}
nomes_usuarios = {}

funil_boas_vindas = """
Você é Dany 🏋️‍♀️, uma consultora de emagrecimento leve, simpática e vendedora.
Seu objetivo principal é vender os produtos SB2 Turbo e SB2 Black, explicando os benefícios com entusiasmo e naturalidade.
Sempre que souber o nome da cliente, use com carinho no início das respostas, como se fosse uma amiga acompanhando a jornada dela.
"""

def extrair_nome(mensagem):
    padroes = [
        r"me chamo ([a-zA-Zà-ü]+)",
        r"sou a ([a-zA-Zà-ü]+)",
        r"aqui é a ([a-zA-Zà-ü]+)",
        r"meu nome é ([a-zA-Zà-ü]+)"
    ]
    for padrao in padroes:
        match = re.search(padrao, mensagem.lower())
        if match:
            nome = match.group(1).capitalize()
            return nome
    return None

def gerar_resposta_dany(pergunta, usuario):
    try:
        nome_detectado = extrair_nome(pergunta)
        if nome_detectado:
            nomes_usuarios[usuario] = nome_detectado

        nome_cliente = nomes_usuarios.get(usuario)
        saudacao_nome = f"{nome_cliente}, " if nome_cliente else ""

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

        if nome_cliente:
            texto = re.sub(r"^(ol[áa]!|oi!?)", f"\\g<0> {nome_cliente}!", texto, flags=re.IGNORECASE)

        contexto_usuario.append({"role": "user", "content": pergunta})
        contexto_usuario.append({"role": "assistant", "content": texto})
        usuarios[usuario] = contexto_usuario[-10:]

        return texto

    except Exception as e:
        print(f"[ERRO] Falha ao gerar resposta: {str(e)}")
        return "⚠️ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


