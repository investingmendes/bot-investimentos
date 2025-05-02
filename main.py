import os
from telegram.ext import MessageHandler  # Adicione esta linha
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Carrega variáveis de ambiente
load_dotenv()

# Importa módulos de análise
from fundamentalista import analisar_fundamentalista
from bazin import calcular_bazin

# Configurações
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia mensagem de boas-vindas com menu de opções"""
    keyboard = [
        [InlineKeyboardButton("Análise Fundamentalista", callback_data='fundamentalista')],
        [InlineKeyboardButton("Método Bazin", callback_data='bazin')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '🤖 Bot de Investimentos\n\nEscolha uma opção:',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa os cliques nos botões"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'fundamentalista':
        await query.edit_message_text(text="📊 Digite o código do ativo (ex: PETR4) para análise fundamentalista:")
        context.user_data['awaiting_input'] = 'fundamentalista'
    elif query.data == 'bazin':
        await query.edit_message_text(text="🧮 Digite o código do ativo (ex: PETR4) para cálculo do Método Bazin:")
        context.user_data['awaiting_input'] = 'bazin'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa as mensagens após seleção de opção"""
    user_data = context.user_data
    if 'awaiting_input' not in user_data:
        await start(update, context)
        return
    
    ticker = update.message.text.upper()
    
    if user_data['awaiting_input'] == 'fundamentalista':
        analysis = analisar_fundamentalista(ticker)
        await update.message.reply_text(analysis)
    elif user_data['awaiting_input'] == 'bazin':
        result = calcular_bazin(ticker)
        await update.message.reply_text(result)
    
    # Limpa o estado
    user_data.pop('awaiting_input', None)
    await start(update, context)

def main():
    """Inicia o bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()