from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import re

app = Flask(__name__)
CORS(app)

openai.api_key = "SUA_CHAVE_API_OPENAI"

# Variável de controle para evitar repetir "Oi" ou "Olá" constantemente
saudou_usuario = False

def gerar_resposta(mensagem):
    global saudou_usuario

    mensagem = mensagem.lower()

    # Detecção de saudação inicial
    saudacoes_iniciais = ["oi", "olá", "boa tarde", "bom dia", "boa noite"]
    if any(saud in mensagem for saud in saudacoes_iniciais) and not saudou_usuario:
        saudou_usuario = True
        return "Oi! 😊 Seja muito bem-vinda! Eu sou a Dany, consultora de emagrecimento. Posso te ajudar a transformar seu corpo com os produtos SB2 Turbo e SB2 Black. Você gostaria de saber como eles funcionam?"

    # Função para resetar saudação quando necessário
    if any(kw in mensagem for kw in ["reiniciar", "resetar"]):
        saudou_usuario = False
        return "Conversa reiniciada! Pode me chamar com suas dúvidas. 😊"

    # Respostas específicas
    if "como comprar" in mensagem or "como faço pra comprar" in mensagem:
        return ("Para comprar o SB2 Turbo ou SB2 Black, basta acessar os links abaixo conforme sua preferência:\n"
                "• SB2 Turbo: https://mmecoser.com/sb2turbo\n"
                "• SB2 Black: https://mmecoser.com/sb2black\n"
                "Caso tenha dúvidas durante a compra, estou aqui pra ajudar! 😊")

    if "quantos dias" in mensagem or "prazo de entrega" in mensagem:
        return ("📦 O prazo médio de entrega é de 5 a 9 dias úteis, dependendo da sua região. E o melhor: o frete é grátis na promoção de hoje!")

    if "interior" in mensagem or "zona rural" in mensagem:
        return ("📦 Pode ficar tranquila, os produtos SB2 Turbo e SB2 Black são entregues em todo o Brasil, inclusive no interior e zona rural. Basta preencher corretamente o endereço no site oficial e o pedido será entregue nos correios da sua cidade!")

    if "diferença entre" in mensagem or "qual a diferença" in mensagem:
        return ("💊 O SB2 Turbo é ideal pra quem quer energia e acelerar a queima de gordura. Já o SB2 Black é ótimo pra controlar o apetite e reduzir medidas. Você busca mais energia ou mais controle do apetite?")

    if "sb2 turbo" in mensagem and "black" in mensagem and "mais indicado" in mensagem:
        return ("😊 Entendo sua dúvida! Tanto o SB2 Turbo quanto o SB2 Black são super eficazes. O SB2 Black é mais concentrado, ideal pra quem busca uma ação mais rápida. Já o Turbo é ótimo pra emagrecimento gradual. Me conta: qual sua meta?")

    if re.search(r"perder.*(\d+).*kg", mensagem):
        match = re.search(r"perder.*?(\d+)", mensagem)
        if match:
            kg = int(match.group(1))
            if kg >= 15:
                return (f"Para perder {kg}kg, o SB2 Turbo pode ser seu melhor aliado! Ele acelera o metabolismo e queima gordura de forma eficaz. Acesse: https://mmecoser.com/sb2turbo")
            else:
                return (f"Para perder {kg}kg, ambos os produtos podem te ajudar, mas o SB2 Turbo costuma ter ação mais rápida. Quer conhecer mais? https://mmecoser.com/sb2turbo")

    if "como funciona" in mensagem and "após a compra" in mensagem or "depois da compra" in mensagem:
        return ("Depois da compra, você receberá a confirmação no seu e-mail com o prazo de entrega e código de rastreio. Eu continuo aqui pra te apoiar com dicas, orientações e acompanhamento personalizado no seu processo de emagrecimento! 💚")

    if "garantia" in mensagem or "posso confiar" in mensagem:
        return ("Sim! A compra é feita diretamente no site oficial e conta com 7 dias de garantia. Se não ficar satisfeita, devolvemos 100% do valor. Compra sem riscos! ✨")

    if "compulsão" in mensagem and "doce" in mensagem:
        return ("Tanto o SB2 Turbo quanto o SB2 Black ajudam a controlar a ansiedade e reduzir a vontade de comer doces. São naturais, com ação detox e controle de apetite. Saiba mais:\n"
                "SB2 Turbo: https://mmecoser.com/sb2turbo\nSB2 Black: https://mmecoser.com/sb2black")

    if any(x in mensagem for x in ["não entendi", "não faz sentido", "isso não ajuda", "não respondeu"]):
        return ("Poxa! Parece que não consegui te ajudar como esperava 😢 Mas não se preocupe, posso te encaminhar para um atendente humano. Deseja seguir com o atendimento agora?")

    # Resposta padrão
    return ("Me conta um pouquinho mais sobre sua meta de emagrecimento? Posso te indicar o melhor produto pra você com base no seu objetivo. 💬")


@app.route("/dany", methods=["POST"])
def webhook():
    dados = request.get_json()
    mensagem = dados.get("mensagem")
    resposta = gerar_resposta(mensagem)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)




