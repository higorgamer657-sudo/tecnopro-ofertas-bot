
import asyncio
import json
import os
from pathlib import Path
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL = "@TecnoPro0fertas"

ARQUIVO_HISTORICO = Path("ofertas_publicadas.json")

# Ofertas de exemplo. Ainda nao sao buscadas automaticamente.

OFERTAS = []

# Configuracoes de selecao das ofertas
PRIORIDADE_TECNOLOGIA = 70
PRIORIDADE_OUTRAS_CATEGORIAS = 30

# Quantidade maxima de ofertas por execucao
MAX_OFERTAS_POR_EXECUCAO = 2

# Categorias prioritarias
PALAVRAS_TECNOLOGIA = [
    "ssd", "processador", "placa de video",
    "memoria ram", "placa mae", "fonte",
    "monitor", "teclado", "mouse",
    "notebook", "computador", "celular",
    "smartphone", "headset", "roteador"
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
    if oferta.get("preco") is None or not oferta.get("link"):
        return None

    nome = oferta["nome"]
    loja = oferta["loja"]
    preco = oferta["preco"]
    preco_antigo = oferta.get("preco_antigo")
    cupom = oferta.get("cupom")
    link = oferta["link"]

    mensagem = (
        "🔥 TECNOPRO OFERTAS 🔥\n\n"
        f"📦 {nome}\n\n"
        f"🛒 Loja: {loja}\n"
    )

    if preco_antigo is not None:
        mensagem += f"❌ De: R$ {preco_antigo:.2f}\n"

    mensagem += f"💰 Por: R$ {preco:.2f}\n"

    if cupom:
        mensagem += f"🏷️ Cupom: {cupom}\n"

    mensagem += f"\n🔗 Comprar: {link}"

    return mensagem


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
