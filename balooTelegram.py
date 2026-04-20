import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from BalooBrain import procesar

TOKEN = os.getenv ("8726225258:AAGxNgGdE49I1-bz5u8-NYoU2amHHL20Ra4") or "8726225258:AAGxNgGdE49I1-bz5u8-NYoU2amHHL20Ra4"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    respuesta = procesar(texto)

    if isinstance(respuesta, str) and os.path.isfile(respuesta):
        with open(respuesta, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text(respuesta)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, responder))
app.run_polling()
