
import asyncio
import json
import os
from pathlib import Path
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL = "@TecnoPro0fertas"

ARQUIVO_HISTORICO = Path("ofertas_publicadas.json")

# Ofertas de exemplo. Ainda nao sao buscadas automaticamente.
OFERTAS = [
    {
        "nome": "SSD Kingston NV3 1TB",
        "loja": "Mercado Livre",
        "preco": None,
        "link": ""
    }
]


def carregar_historico():
    if ARQUIVO_HISTORICO.exists():
        return set(json.loads(
            ARQUIVO_HISTORICO.read_text(encoding="utf-8")
        ))
    return set()


def salvar_historico(historico):
    ARQUIVO_HISTORICO.write_text(
        json.dumps(sorted(historico), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def preparar_mensagem(oferta):
    if oferta["preco"] is None or not oferta["link"]:
        return None

    return (
        "🔥 TECNOPRO OFERTAS\n\n"
        f"📦 {oferta['nome']}\n"
        f"🏪 Loja: {oferta['loja']}\n"
        f"💰 Preço: R$ {oferta['preco']:.2f}\n\n"
        f"🛒 Comprar: {oferta['link']}"
    )


async def main():
    if not TOKEN:
        raise RuntimeError("Token nao configurado.")

    historico = carregar_historico()
    novas_ofertas = []

    for oferta in OFERTAS:
        mensagem = preparar_mensagem(oferta)

        if not mensagem:
            continue

        identificador = f"{oferta['link']}|{oferta['preco']}"

        if identificador not in historico:
            novas_ofertas.append((identificador, mensagem))

    if not novas_ofertas:
        print("Nenhuma oferta nova para publicar.")
        return

    async with Bot(TOKEN) as bot:
        for identificador, mensagem in novas_ofertas:
            await bot.send_message(chat_id=CANAL, text=mensagem)
            historico.add(identificador)
            salvar_historico(historico)

    print("Ofertas publicadas com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
