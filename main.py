from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from dotenv import load_dotenv
import os

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Obtém o token da variável de ambiente
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot funcionando! ✅')

def main():
    # 3. Verifica se o token existe
    if not TOKEN:
        print("❌ Erro: Token não encontrado!")
        return
    
    # 4. Configura o bot
    application = ApplicationBuilder().token(TOKEN).build()
    
    # 5. Adiciona os comandos
    application.add_handler(CommandHandler("start", start))
    
    print("🟢 Iniciando bot...")
    application.run_polling()

if __name__ == '__main__':
    main()