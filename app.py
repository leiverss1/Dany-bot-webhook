from flask import Flask, request, jsonify
import openai
import os
from datetime import datetime
import re

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

sessoes = {}

@app.route('/')
def home():
    return '🤖 Dany AI - Webhook funcionando com OpenAI!'

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
    mensagem = dados.get("mensagem", "")
    usuario = dados.get("usuario", "desconhecido")

    if not mensagem:
        return jsonify({"resposta": "Mensagem vazia."}), 400

    sessao = sessoes.get(usuario, {"nome": None, "dor": None, "perfil": None})

    # Captura nome
    if not sessao["nome"]:
        nome_match = re.search(r"(?i)me chamo ([A-Za-zÀ-ÿ]+)|sou a ([A-Za-zÀ-ÿ]+)|aqui é a ([A-Za-zÀ-ÿ]+)", mensagem)
        if nome_match:
            grupos = nome_match.groups()
            sessao["nome"] = next((g for g in grupos if g), None)

    # Detecta dor
    if not sessao["dor"]:
        if re.search(r"(?i)perder barriga|abd[oô]men|incha[çc]o", mensagem):
            sessao["dor"] = "perder barriga"
        elif re.search(r"(?i)apetite|fome|compuls[ãa]o", mensagem):
            sessao["dor"] = "controlar apetite"
        elif re.search(r"(?i)emagrecer|perder peso|eliminar kg", mensagem):
            sessao["dor"] = "emagrecer"

    # Detecta perfil especial
    if not sessao["perfil"]:
        if re.search(r"(?i)filhos|m[ãa]e|correria|rotina|trabalho", mensagem):
            sessao["perfil"] = "mãe ocupada"
        elif re.search(r"(?i)54 anos|idade|menopausa|lento|metabolismo", mensagem):
            sessao["perfil"] = "idade/metabolismo lento"
        elif re.search(r"(?i)vestido|evento|casamento", mensagem):
            sessao["perfil"] = "evento próximo"
        elif re.search(r"(?i)vegetariana|vegano|vegana|natural", mensagem):
            sessao["perfil"] = "vegetariana"
        elif re.search(r"(?i)autoestima|triste|depress[ãa]o|corpo|espelho", mensagem):
            sessao["perfil"] = "autoestima"

    sessoes[usuario] = sessao

    resposta = gerar_resposta_dany(mensagem, sessao)
    return jsonify({"resposta": resposta})

def gerar_resposta_dany(mensagem, sessao):
    nome = sessao.get("nome")
    dor = sessao.get("dor")
    perfil = sessao.get("perfil")

    contexto = f"Nome da cliente: {nome or 'não informado'}.\n"
    contexto += f"Dor principal: {dor or 'não detectada'}.\n"
    contexto += f"Perfil identificado: {perfil or 'não detectado'}.\n"

    prompt = f"""
Você é Dany, uma consultora de emagrecimento simpática, humana, divertida e vendedora.

Seu papel é acolher a cliente com empatia e alegria, entender a dor ou objetivo dela, e então recomendar o produto SB2 mais adequado (Turbo ou Black), com leveza, explicação e naturalidade.

Regras:
- Nunca comece cada resposta com "olá" ou "oi" se já houver conversa.
- Se a cliente disser que quer emagrecer, perder barriga, controlar apetite ou melhorar autoestima, acolha primeiro, incentive, depois recomende o produto.
- Se identificar um perfil especial (mãe ocupada, menopausa, autoestima, vegana, evento próximo), use isso para personalizar a resposta.
- Após recomendar, envie link com cuidado e simpatia.
- Finalize com incentivo (ex: você consegue, tô com você, vai dar certo).

{contexto}
Mensagem da cliente: {mensagem}
Responda como Dany:
"""

    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": mensagem}
            ]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERRO] Falha ao gerar resposta: {str(e)}")
        return "❌ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



