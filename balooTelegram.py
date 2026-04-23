import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from BalooBrain import procesar


# 🔐 TOKEN (Railway o fallback local)
TOKEN = os.getenv("TELEGRAM_TOKEN") or "8726225258:AAGxNgDdE49I1-bz5u8-NYoU2amHHL20Ra4"

print("BOT INICIADO 🔥")


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = update.message.text

        print("MENSAJE RECIBIDO:", texto)

        respuesta = procesar(texto)

        print("RESPUESTA:", respuesta)

        # 📄 Si es archivo → enviarlo
        if isinstance(respuesta, str) and respuesta.endswith(".docx") and os.path.isfile(respuesta):
            with open(respuesta, "rb") as f:
                await update.message.reply_document(document=f)
        else:
            await update.message.reply_text(respuesta)

    except Exception as e:
        print("ERROR EN BOT:", str(e))
        await update.message.reply_text("❌ Ocurrió un error")


# 🚀 INICIAR BOT
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("BOT CORRIENDO 🚀")

app.run_polling()
