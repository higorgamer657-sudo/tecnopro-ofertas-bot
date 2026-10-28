
import asyncio
import os
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL = "@TecnoPro0fertas"

async def main():
    if not TOKEN:
        raise RuntimeError("Token não configurado.")

    async with Bot(TOKEN) as bot:
        await bot.send_message(
            chat_id=CANAL,
            text=(
                "🚀 TECNOPRO OFERTAS\n\n"
                "Teste de publicação pela nuvem! 💙\n"
                "Nosso sistema está sendo preparado."
            )
        )

    print("Publicação realizada com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
