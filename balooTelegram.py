import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from BalooBrain import procesar

TOKEN = os.getenv("8726225258:AAGxNgGdE49I1-bz5u8-NYoU2amHHL20Ra4")


def ejecutar_agente(texto):
    return procesar(texto)


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text
    
    respuesta = ejecutar_agente(mensaje_usuario)

    print("RESPUESTA:", respuesta)  # 👈 debug

    # 🔥 AQUÍ PASA LA MAGIA
    if os.path.exists(respuesta):
        with open(respuesta, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text(respuesta)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, responder))

app.run_polling()
