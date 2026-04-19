
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8726225258:AAGxNgGdE49I1-bz5u8-NYoU2amHHL20Ra4"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text
    
    respuesta = ejecutar_agente(mensaje_usuario)
    
    await update.message.reply_text(respuesta)



from BalooBrain import procesar
def ejecutar_agente(texto):
    return procesar(texto)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, responder))

app.run_polling()