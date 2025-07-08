import { create } from 'venom-bot';
import axios from 'axios';

create({
  session: 'dany-session',
  browserPathExecutable: "C:\\Program Files\\Google\\Google Chrome\\Application\\chrome.exe",
  headless: false
}).then((client) => start(client));

function start(client) {
  client.onMessage(async (message) => {
    if (message.isGroupMsg === false) {
      const msg = message.body.toLowerCase();
      let resposta = '';

      // Etapas do funil de vendas e dúvidas comuns
      if (msg.includes("oi") || msg.includes("olá") || msg.includes("bom dia") || msg.includes("boa tarde") || msg.includes("boa noite")) {
        resposta = "Oi! 😊 Seja muito bem-vinda! Eu sou a Dany, consultora de emagrecimento. Posso te ajudar a transformar seu corpo com os produtos SB2 Turbo e SB2 Black. Você gostaria de saber como eles funcionam?";
      } else if (msg.includes("como funciona") || msg.includes("quero saber mais") || msg.includes("me explica")) {
        resposta = "✨ O SB2 Turbo e o SB2 Black são suplementos naturais que ajudam a acelerar o metabolismo, reduzir o inchaço e queimar gordura. Você gostaria de saber qual deles é o ideal pra você?";
      } else if (msg.includes("qual o melhor") || msg.includes("diferença")) {
        resposta = "📌 O SB2 Turbo é ideal pra quem quer energia e acelerar a queima de gordura. Já o SB2 Black é ótimo pra controlar o apetite e reduzir medidas. Você busca mais energia ou mais controle do apetite?";
      } else if (msg.includes("quero comprar") || msg.includes("como compro")) {
        resposta = "🎯 Maravilha! Temos uma oferta especial com FRETE GRÁTIS e bônus. E o melhor: mais de 12.000 mulheres já transformaram o corpo com nossos produtos! 💪 Posso te enviar o link pra garantir o seu?";
      } else if (msg.includes("sim") || msg.includes("pode enviar")) {
        resposta = "🚀 Aqui está o link pra você garantir sua transformação agora mesmo 👉 https://mmecoserv.com/sb2turbo 💖 Ou, se preferir o SB2 Black, acesse 👉 https://mmecoserv.com/sb2black";
      } else if (msg.includes("garantia")) {
        resposta = "Claro! Você tem 7 dias de garantia após a compra. Se não ficar satisfeita, devolvemos 100% do valor. 😌✨ Compra sem riscos!";
      } else if (msg.includes("funciona mesmo") || msg.includes("funciona de verdade")) {
        resposta = "Sim! 🟢 Mais de 12.000 mulheres já tiveram resultados reais com SB2 Turbo e SB2 Black. A fórmula é natural, aprovada pela Anvisa e com resultados visíveis em até 7 dias!";
      } else if (msg.includes("efeitos colaterais") || msg.includes("faz mal")) {
        resposta = "Não. 💚 Os produtos são 100% naturais, sem química pesada, e não causam efeitos colaterais. Inclusive, muitas clientes relatam melhora na disposição e no humor!";
      } else if (msg.includes("amamentando") || msg.includes("grávida")) {
        resposta = "Se você está grávida ou amamentando, o ideal é conversar com seu médico antes de tomar qualquer suplemento, mesmo natural. Segurança em primeiro lugar! 🤱✨";
      } else if (msg.includes("entrega") || msg.includes("prazo") || msg.includes("chega quando")) {
        resposta = "📦 O prazo médio de entrega é de 5 a 9 dias úteis, dependendo da sua região. E o melhor: o frete é grátis na promoção de hoje!";
      } else if (msg.includes("contraindicação")) {
        resposta = "Os produtos são naturais, mas não são indicados para gestantes, lactantes e pessoas com restrições severas. Em caso de dúvida, consulte um profissional de saúde. 💊✅";
      } else {
        // Se não for um gatilho, envia para a API (OpenAI)
        try {
          const retorno = await axios.post('https://dany-bot-webhook.onrender.com/dany', {
            mensagem: message.body,
            usuario: message.from
          });
          resposta = retorno.data.resposta;
        } catch (error) {
          console.error('Erro ao enviar para a API:', error.message);
          resposta = '⚠️ Ocorreu um erro. Tente novamente.';
        }
      }

      await client.sendText(message.from, resposta);
    }
  });
}



