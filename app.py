# app.py
from flask import Flask, request, jsonify
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configurações
FACEBOOK_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("WEBHOOK_VERIFY_TOKEN")
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0"

class DanyAI:
    def __init__(self):
        self.produtos = {
            "sb2_turbo": {
                "nome": "SB2 Turbo",
                "link": "https://mmecoserv.com/sb2turbo",
                "preco": "12x de R$ 29,90",
                "beneficios": ["Controla apetite", "Aumenta energia", "Reduz medidas", "Natural 100%"]
            },
            "sb2_black": {
                "nome": "SB2 Black",
                "link": "https://mmecoserv.com/sb2black",
                "preco": "Promoção especial",
                "beneficios": ["Emagrecimento acelerado", "Queima gordura", "Mais disposição", "Grupo VIP"]
            }
        }

    def gerar_resposta(self, mensagem, usuario):
        mensagem_lower = mensagem.lower()

        if any(s in mensagem_lower for s in ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite']):
            return """🌟 Olá! Eu sou a Dany, sua consultora especialista em emagrecimento!
Como posso te ajudar hoje?
📱 Quer conhecer nossos produtos naturais?
💪 Precisa de ajuda para emagrecer?
🎯 Tem alguma meta específica?
Digite *PRODUTOS* para ver nossas opções ou me conte um pouco sobre seus objetivos! 💖"""

        elif 'produto' in mensagem_lower or 'sb2' in mensagem_lower:
            return """🔥 NOSSOS PRODUTOS DE SUCESSO:
🌟 *SB2 TURBO* - O Mais Popular!
✅ Controla apetite naturalmente
✅ Aumenta energia e disposição
✅ Reduz medidas rapidamente
💰 Apenas 12x de R$ 29,90

🚀 *SB2 BLACK* - Fórmula Premium!
✅ Emagrecimento acelerado
✅ Queima gordura localizada
✅ Resultados em até 15 dias
🎁 + Grupo VIP + E-books grátis
Qual produto desperta mais seu interesse?
Digite *1* para SB2 Turbo ou *2* para SB2 Black"""

        elif '1' in mensagem or 'turbo' in mensagem_lower:
            return f"""🌟 *SB2 TURBO - EXCELENTE ESCOLHA!*
🎯 *BENEFÍCIOS COMPROVADOS:*
• Controla a fome e compulsão
• Aumenta energia para o dia todo
• Acelera queima de gordura
• 100% natural e seguro
💰 *INVESTIMENTO:* 12x de R$ 29,90
🚚 *FRETE GRÁTIS* para todo Brasil
⚡ *ENTREGA EXPRESSA* em 3-5 dias
*LINK EXCLUSIVO:* {self.produtos['sb2_turbo']['link']}
Quer que eu tire alguma dúvida específica sobre o SB2 Turbo? 💪"""

        elif '2' in mensagem or 'black' in mensagem_lower:
            return f"""🚀 *SB2 BLACK - FÓRMULA PREMIUM!*
🔥 *RESULTADOS POTENCIALIZADOS:*
• Emagrecimento até 3x mais rápido
• Queima gordura localizada
• Energia e disposição máxima
• Fórmula exclusiva premium
🎁 *BÔNUS EXCLUSIVOS:*
• Grupo VIP com acompanhamento
• 2 E-books de receitas
• Desafio 21 dias para emagrecer
*APROVEITE A PROMOÇÃO:* {self.produtos['sb2_black']['link']}
Pronta para sua transformação completa? 🌟"""

        elif any(p in mensagem_lower for p in ['como', 'funciona', 'tomar', 'usar']):
            return """💊 *COMO USAR:*
• 2 cápsulas ao dia
• 1 antes do almoço + 1 antes do jantar
• Com um copo de água
• Use por 3-6 meses para resultados duradouros
⏰ *QUANDO VER RESULTADOS:*
• Primeiros 7 dias: Menos fome
• 15 dias: Mais energia
• 30 dias: Medidas reduzindo
• 60-90 dias: Transformação completa"""

        elif any(p in mensagem_lower for p in ['preço', 'valor', 'quanto', 'custa']):
            return """💰 *NOSSOS INVESTIMENTOS:*
🌟 *SB2 TURBO:* 12x R$ 29,90
🚀 *SB2 BLACK:* Promoção especial no site
🎁 *VANTAGENS:*
✅ Frete grátis para todo Brasil
✅ Garantia de 30 dias
✅ Suporte personalizado
✅ Acompanhamento pós-venda
*Qual cabe melhor no seu orçamento?*
• SB2 Turbo: https://mmecoserv.com/sb2turbo
• SB2 Black: https://mmecoserv.com/sb2black"""

        elif any(p in mensagem_lower for p in ['acompanhamento', 'coaching', 'ajuda', 'suporte']):
            return """👩‍⚕️ *ACOMPANHAMENTO COMPLETO:*
🎯 *O QUE VOCÊ TEM DIREITO:*
• Suporte 24/7 via WhatsApp
• Dicas diárias personalizadas
• Acompanhamento de resultados
• Motivação e incentivo constante
• Grupo VIP com outras clientes"""

        elif any(p in mensagem_lower for p in ['caro', 'barato', 'desconto']):
            return """💰 *VAMOS FAZER UMA CONTA RÁPIDA:*
☕ Café diário: R$ 5 x 30 = R$ 150/mês
🍔 Fast food: R$ 25 x 4 = R$ 100/mês
💊 SB2 Turbo: R$ 29,90/mês
*Ou seja, menos que um café por dia para:*
✅ Conquistar o corpo dos sonhos
✅ Ter mais saúde e energia
✅ Elevar sua autoestima
✅ Transformar sua vida"""

        elif any(p in mensagem_lower for p in ['resultado', 'funciona', 'depoimento']):
            return """📈 *RESULTADOS REAIS DE CLIENTES:*
👩 Maria, 34 anos: "Perdi 8kg em 2 meses!"
👩 Ana, 28 anos: "Nunca tive tanta energia!"
👩 Julia, 42 anos: "Finalmente controlo minha fome!"
👩 Carla, 35 anos: "Minha autoestima voltou!"""

        return """💖 *Estou aqui para te ajudar!*
Posso esclarecer sobre:
🔹 Nossos produtos (digite *PRODUTOS*)
🔹 Como funciona (digite *COMO USAR*)
🔹 Valores (digite *PREÇO*)
🔹 Resultados (digite *RESULTADOS*)
🔹 Acompanhamento (digite *COACHING*)
Ou me conte: qual é seu principal objetivo com o emagrecimento? 😊"""

dany = DanyAI()

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        mode = request.args.get('hub.mode')
        if token == VERIFY_TOKEN and mode == "subscribe":
            return str(challenge), 200
        return 'Token inválido', 403

    elif request.method == 'POST':
        data = request.get_json()
        print("Webhook recebido:", json.dumps(data, indent=2))
        if 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    if change.get('field') == 'messages':
                        value = change.get('value', {})
                        for message in value.get('messages', []):
                            processar_mensagem(message, value)
        return 'OK', 200

def processar_mensagem(message, value):
    try:
        usuario_id = message['from']
        mensagem_texto = message.get('text', {}).get('body', '')
        print(f"Mensagem de {usuario_id}: {mensagem_texto}")
        resposta = dany.gerar_resposta(mensagem_texto, usuario_id)
        enviar_mensagem(usuario_id, resposta)
        print(f"Resposta enviada: {resposta[:100]}...")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def enviar_mensagem(usuario_id, mensagem):
    url = f"{WHATSAPP_API_URL}/messages"
    headers = {
        'Authorization': f'Bearer {FACEBOOK_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": usuario_id,
        "text": {"body": mensagem}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Resposta do WhatsApp:", response.status_code, response.text)
    return response.json()

@app.route('/')
def home():
    return '🤖 Dany AI - Webhook Ativo!'

@app.route('/status')
def status():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'webhook': 'ativo'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
