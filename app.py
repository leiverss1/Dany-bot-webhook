from flask import Flask, request, jsonify
import openai
import os
from datetime import datetime

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Armazenar nome e dor da cliente por sessão simples (exemplo para testes)
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

    sessao = sessoes.get(usuario, {"nome": None, "dor": None})

    # Captura nome se contiver "sou a" ou "me chamo"
    if not sessao["nome"]:
        if "sou a " in mensagem.lower() or "me chamo " in mensagem.lower():
            partes = mensagem.split()
            for i, palavra in enumerate(partes):
                if palavra.lower() in ["sou", "sou", "chamo"] and i + 1 < len(partes):
                    nome = partes[i + 1].capitalize()
                    sessao["nome"] = nome
                    break

    # Captura dor (emagrecer, perder barriga, controlar apetite)
    if not sessao["dor"]:
        if any(p in mensagem.lower() for p in ["emagrecer", "perder peso", "perder barriga"]):
            sessao["dor"] = "perder barriga"
        elif "apetite" in mensagem.lower():
            sessao["dor"] = "controlar apetite"

    sessoes[usuario] = sessao

    resposta = gerar_resposta_dany(mensagem, sessao)
    return jsonify({"resposta": resposta})

def gerar_resposta_dany(mensagem, sessao):
    nome = sessao.get("nome")
    dor = sessao.get("dor")

    prompt_base = f"""
Você é a Dany, uma consultora de emagrecimento simpática, natural, envolvente e divertida. 

Sempre que possível, use o nome da cliente (se souber) e mencione a dor dela (como perder barriga ou controlar apetite).

Seu objetivo principal é **vender os produtos SB2 Turbo e SB2 Black**, e usar gatilhos como:
- Frete grátis
- Resultados reais
- Segurança e naturalidade
- Aprovação e garantia
- Confiança na compra

Quando perguntarem se entrega em alguma cidade, sempre responda com carinho mencionando a cidade e dizendo que entrega em todo o Brasil.

Ao final da conversa, mantenha contato amigável, e se possível continue dando dicas mesmo depois da compra para gerar recompra futura.

Nunca reinicie a conversa com "Olá" em toda resposta. Mantenha o tom humano e de continuidade.

Cliente: {mensagem}

Contexto conhecido:
- Nome: {nome or "não informado"}
- Dor: {dor or "não identificada"}

Responda como Dany:
"""
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_base},
                {"role": "user", "content": mensagem}
            ]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERRO] Falha na geração de resposta: {str(e)}")
        return "❌ Ocorreu um erro ao gerar a resposta. Tente novamente mais tarde."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



