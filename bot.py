
import asyncio
import os
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL = "@TecnoPro0fertas"

# Ofertas cadastradas para teste
# No futuro, esta lista sera alimentada automaticamente.
OFERTAS = [
    {
        "nome": "SSD Kingston NV3 1TB",
        "loja": "Mercado Livre",
        "preco": None,
        "link": ""
    }
]


def preparar_mensagem(oferta):
    nome = oferta["nome"]
    loja = oferta["loja"]
    preco = oferta["preco"]
    link = oferta["link"]

    if preco is None or not link:
        return None

    return (
        f"🔥 TECNOPRO OFERTAS\n\n"
        f"📦 {nome}\n"
        f"🏪 Loja: {loja}\n"
        f"💰 Preço: R$ {preco:.2f}\n\n"
        f"🛒 Comprar: {link}"
    )


async def main():
    if not TOKEN:
        raise RuntimeError("Token nao configurado.")

    mensagens = []

    for oferta in OFERTAS:
        mensagem = preparar_mensagem(oferta)
        if mensagem:
            mensagens.append(mensagem)

    if not mensagens:
        print("Nenhuma oferta completa para publicar.")
        return

    async with Bot(TOKEN) as bot:
        for mensagem in mensagens:
            await bot.send_message(
                chat_id=CANAL,
                text=mensagem
            )

    print("Ofertas publicadas com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
