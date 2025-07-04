# app.py
from flask import Flask, request, jsonify
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Configurações
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
WEBHOOK_VERIFY_TOKEN = os.environ.get('WEBHOOK_VERIFY_2024', 'DANY_WEBHOOK_2024')
WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '5511970241011')

# Links de afiliado
AFFILIATE_LINKS = {
    'sb2_turbo': 'https://mmecoserv.com/sb2turbo',
    'sb2_black': 'https://mmecoserv.com/sb2black'
}

# Personalidade da Dany
DANY_PERSONALITY = {
    'name': 'Dany',
    'role': 'Especialista em Emagrecimento e Coach de Bem-estar',
    'tone': 'amigável, motivadora e profissional',
    'expertise': 'produtos naturais para emagrecimento, SB2 Turbo e SB2 Black'
}

# Função de log
def log_message(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

# Função para enviar mensagens no WhatsApp
def send_whatsapp_message(recipient, message):
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_NUMBER}/messages"
    headers = {
        'Authorization': f'Bearer {FACEBOOK_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'messaging_product': 'whatsapp',
        'to': recipient,
        'type': 'text',
        'text': {'body': message}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        log_message(f"Mensagem enviada para {recipient}: {response.status_code}")
        return response.json()
    except Exception as e:
        log_message(f"Erro ao enviar mensagem: {str(e)}", "ERROR")
        return None

# Função para processar mensagens recebidas
def process_dany_message(sender, message_text):
    message_lower = message_text.lower()
    
    if any(word in message_lower for word in ['oi', 'olá', 'ola', 'hey', 'bom dia', 'boa tarde', 'boa noite']):
        return """..."""  # Use o conteúdo detalhado do seu texto original

    elif any(word in message_lower for word in ['produto', 'emagrecer', 'perder peso', 'sb2', 'turbo', 'black']):
        return """..."""

    elif '1' in message_text or 'turbo' in message_lower:
        return f"""Excelente escolha! 🚀 O SB2 Turbo é nosso bestseller! ... {AFFILIATE_LINKS['sb2_turbo']}"""

    elif '2' in message_text or 'black' in message_lower:
        return f"""Perfeita escolha! 🖤 O SB2 Black é nossa fórmula premium! ... {AFFILIATE_LINKS['sb2_black']}"""

    elif any(word in message_lower for word in ['seguro', 'efeito colateral', 'natural', 'anvisa']):
        return """Pode ficar tranquila! 😊 Nossa prioridade é sua segurança! ..."""

    elif any(word in message_lower for word in ['preço', 'valor', 'quanto custa', 'promoção']):
        return f"""Ótima pergunta! 💰 Temos condições especiais! ... {AFFILIATE_LINKS['sb2_turbo']} {AFFILIATE_LINKS['sb2_black']}"""

    elif any(word in message_lower for word in ['caro', 'pensar', 'depois', 'não tenho dinheiro']):
        return f"""Entendo perfeitamente! 💝 ... {AFFILIATE_LINKS['sb2_turbo']} - SB2 Turbo {AFFILIATE_LINKS['sb2_black']} - SB2 Black"""

    elif any(word in message_lower for word in ['depoimento', 'funciona', 'resultado', 'prova']):
        return f"""Claro! 🌟 Nossos resultados falam por si! ... {AFFILIATE_LINKS['sb2_turbo']} - SB2 Turbo {AFFILIATE_LINKS['sb2_black']} - SB2 Black"""

    else:
        return f"""Obrigada por me procurar! 😊 Sou a Dany ... {AFFILIATE_LINKS['sb2_turbo']} - SB2 Turbo {AFFILIATE_LINKS['sb2_black']} - SB2 Black"""

# Verificação do webhook
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    try:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        log_message(f"Verificação webhook - Mode: {mode}, Token: {token}")
        if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
            log_message("Webhook verificado com sucesso!")
            return challenge
        else:
            log_message("Falha na verificação do webhook", "ERROR")
            return "Forbidden", 403
    except Exception as e:
        log_message(f"Erro na verificação: {str(e)}", "ERROR")
        return "Internal Server Error", 500

# Recebimento de mensagens
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.get_json()
        log_message(f"Webhook recebido: {json.dumps(data, indent=2)}")
        if data.get('object') == 'whatsapp_business_account':
            entries = data.get('entry', [])
            for entry in entries:
                changes = entry.get('changes', [])
                for change in changes:
                    if change.get('field') == 'messages':
                        messages = change.get('value', {}).get('messages', [])
                        for message in messages:
                            sender = message.get('from')
                            message_text = message.get('text', {}).get('body', '')
                            message_type = message.get('type')
                            log_message(f"Mensagem de {sender}: {message_text}")
                            if message_type == 'text' and message_text:
                                response = process_dany_message(sender, message_text)
                                if response:
                                    send_whatsapp_message(sender, response)
                                    log_message(f"Resposta enviada para {sender}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        log_message(f"Erro no webhook: {str(e)}", "ERROR")
        return jsonify({"error": str(e)}), 500

# Rota de verificação de saúde
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "webhook_token": WEBHOOK_VERIFY_TOKEN,
        "whatsapp_number": WHATSAPP_NUMBER
    })

# Rota principal
@app.route('/')
def index():
    return jsonify({
        "message": "Dany WhatsApp Bot está funcionando!",
        "status": "active",
        "endpoints": {
            "webhook": "/webhook",
            "health": "/health"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
