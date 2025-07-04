# app.py
from flask import Flask, request, jsonify
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Configurações
FACEBOOK_ACCESS_TOKEN = os.environ.get('EAAVik7hYLWMBPI85Kk1t1qn97eSI4aDQ76WytsQmxixSFDaxge1JK61AwREp7Fr20skW3vqt6sLFbA12m5G7CphVCDSLD05k7eMZADOAwUDbsuQZBD1iHtcRWnaG41f8c9yd1Grk4wNldD2ZB89rHQwGpfSsVAinkEfyL3kWppejk04slvdgeHZCsodWa7WExVM23Q4Qgdu0uoIugwa34rczxAWDTyuDGEIZB0aSPZAkIMTdpjekPjQTUTCrsLLgZDZD')
WEBHOOK_VERIFY_TOKEN = os.environ.get('WEBHOOK_VERIFY_TOKEN', 'DANY_WEBHOOK_2024')
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '5511970241011')

# Links de afiliado
AFFILIATE_LINKS = {
    'sb2_turbo': 'https://mmecoserv.com/sb2turbo',
    'sb2_black': 'https://mmecoserv.com/sb2black'
}

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Dany Webhook está funcionando!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificação do webhook pelo Meta Developer"""
    try:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
            print(f"Webhook verificado com sucesso! Challenge: {challenge}")
            return challenge
        else:
            print(f"Falha na verificação. Token recebido: {token}")
            return 'Forbidden', 403
            
    except Exception as e:
        print(f"Erro na verificação do webhook: {str(e)}")
        return 'Error', 500

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Processa mensagens recebidas do WhatsApp"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
            
        # Log da mensagem recebida
        print(f"Webhook recebido: {json.dumps(data, indent=2)}")
        
        # Processa mensagens
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change.get('field') == 'messages':
                            process_message(change.get('value', {}))
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"Erro ao processar webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def process_message(message_data):
    """Processa mensagem e responde como Dany"""
    try:
        if 'messages' not in message_data:
            return
            
        for message in message_data['messages']:
            sender_id = message['from']
            message_text = message.get('text', {}).get('body', '').lower()
            
            # Gera resposta da Dany
            response = generate_dany_response(message_text, sender_id)
            
            if response:
                send_whatsapp_message(sender_id, response)
                
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")

def generate_dany_response(message_text, sender_id):
    """Gera resposta inteligente da Dany"""
    
    # Saudações
    if any(word in message_text for word in ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite']):
        return f"""Olá! 😊 Eu sou a Dany, sua consultora especialista em emagrecimento!

🎯 Estou aqui para te ajudar a alcançar seus objetivos de forma saudável e definitiva.

Me conta, qual é seu maior desafio hoje:
1️⃣ Controlar a fome/compulsão?
2️⃣ Acelerar o metabolismo?
3️⃣ Perder medidas rapidamente?
4️⃣ Ter mais energia e disposição?

Responde com o número que mais se identifica! 💪"""

    # Interesse em produtos
    elif any(word in message_text for word in ['1', 'fome', 'compulsao', 'compulsão', 'apetite']):
        return f"""Perfeito! Controlar a fome é essencial para o emagrecimento! 🎯

Para compulsão e controle do apetite, eu recomendo o **SB2 TURBO**:

✅ Controla naturalmente a fome
✅ Reduz a compulsão por doces
✅ Aumenta a saciedade
✅ Regula os níveis de açúcar

👉 **OFERTA ESPECIAL**: {AFFILIATE_LINKS['sb2_turbo']}

Já teve problema com compulsão alimentar antes? Me conta sua experiência! 💬"""

    elif any(word in message_text for word in ['2', 'metabolismo', 'queimar', 'gordura']):
        return f"""Excelente escolha! Acelerar o metabolismo é a chave! 🔥

Para metabolismo acelerado, recomendo o **SB2 BLACK**:

✅ Queima gordura 24h por dia
✅ Acelera o metabolismo
✅ Aumenta a energia
✅ Resultados mais rápidos

👉 **OFERTA ESPECIAL**: {AFFILIATE_LINKS['sb2_black']}

Quantos quilos você gostaria de perder? 📏"""

    # Dúvidas sobre produtos
    elif any(word in message_text for word in ['preco', 'preço', 'valor', 'quanto custa']):
        return """💰 **PREÇOS ESPECIAIS DE HOJE:**

🔥 **SB2 TURBO**: De R$ 297 por 12x de R$ 29,70
🚀 **SB2 BLACK**: De R$ 397 por 12x de R$ 39,70

✅ **BÔNUS EXCLUSIVOS:**
- 2 E-books de emagrecimento
- Grupo VIP com desafio 21 dias
- Acompanhamento personalizado

⚡ **GARANTIA**: 30 dias ou seu dinheiro de volta!

Qual produto te interessou mais? 🤔"""

    # Objeções comuns
    elif any(word in message_text for word in ['funciona', 'resultado', 'tempo']):
        return """🏆 **RESULTADOS COMPROVADOS:**

✅ **Primeiros 7 dias**: Redução da fome e mais energia
✅ **30 dias**: Perda de 3-8kg em média
✅ **60 dias**: Transformação completa

👥 **+ de 60.000 pessoas já transformaram suas vidas!**

🔬 **Ingredientes 100% naturais e aprovados pela ANVISA**

⭐ **Média de 4.9 estrelas em avaliações**

Qual sua maior preocupação? Posso te ajudar! 💪"""

    # Interesse em comprar
    elif any(word in message_text for word in ['quero', 'comprar', 'adquirir', 'link']):
        return f"""🎉 **PERFEITO! Vou te ajudar a escolher o ideal:**

🤔 **Me responde rápido:**
- Seu foco principal é controlar a fome OU acelerar o metabolismo?

**PARA CONTROLE DA FOME:**
👉 SB2 TURBO: {AFFILIATE_LINKS['sb2_turbo']}

**PARA QUEIMAR GORDURA RÁPIDO:**
👉 SB2 BLACK: {AFFILIATE_LINKS['sb2_black']}

🎁 **BÔNUS GARANTIDO**: Grupo VIP + 2 E-books + Acompanhamento

⚡ **ATENÇÃO**: Oferta por tempo limitado!

Qual você escolhe? 🚀"""

    # Mensagem padrão
    else:
        return """Oi! 😊 Sou a Dany, especialista em emagrecimento!

🎯 **Estou aqui para te ajudar com:**
- SB2 TURBO (controle da fome)
- SB2 BLACK (acelera metabolismo)

Digite:
• "QUERO EMAGRECER" para conhecer os produtos
• "PREÇO" para ver ofertas especiais
• "RESULTADOS" para ver depoimentos

Como posso te ajudar hoje? 💪"""

def send_whatsapp_message(to, text):
    """Envia mensagem via WhatsApp Business API"""
    try:
        url = f"https://graph.facebook.com/v17.0/{WHATSAPP_NUMBER}/messages"
        
        headers = {
            'Authorization': f'Bearer {FACEBOOK_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": text}
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print(f"Mensagem enviada com sucesso para {to}")
        else:
            print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Erro ao enviar mensagem: {str(e)}")

@app.route('/health')
def health_check():
    """Health check para monitoramento"""
    return jsonify({
        'status': 'healthy',
        'webhook_token_configured': bool(WEBHOOK_VERIFY_TOKEN),
        'facebook_token_configured': bool(FACEBOOK_ACCESS_TOKEN),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
