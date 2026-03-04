import os
import asyncio
from telethon import TelegramClient, events
from telegram import Bot
import anthropic

# Credentials
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
TOKEN = os.environ.get("TOKEN")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
CHAT_ID = os.environ.get("CHAT_ID")

# Setup
claude = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
bot = Bot(token=TOKEN)

# Daftar channel yang dipantau
CHANNELS = [
    "@cupangventures",
    "@airdropfinder",
    "@airdropnusantaraC",
    "@airdropasc",
    "@AirdropLahat",
    "@airdropdaydua",
    "@bangpateng_airdrop",
    "@garapanjawa",
]

# Fungsi analisa pakai AI
def analisa_airdrop(pesan):
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system="""Kamu adalah AI analyst airdrop crypto. 
        Analisa pesan berikut dan tentukan:
        1. Apakah ini info airdrop? (Ya/Tidak)
        2. Kalau Ya, seberapa menarik? (Tinggi/Sedang/Rendah)
        3. Apa yang harus dilakukan?
        4. Ada red flag penipuan?
        Jawab singkat dan dalam Bahasa Indonesia.""",
        messages=[{"role": "user", "content": pesan}]
    )
    return response.content[0].text

# Fungsi utama pemantau
async def main():
    client = TelegramClient('session', API_ID, API_HASH)
    await client.start()

    print("Agent berjalan! Memantau channel... 🔍")

    @client.on(events.NewMessage(chats=CHANNELS))
    async def handler(event):
        pesan = event.message.text

        if not pesan:
            return

        print("Pesan baru diterima, menganalisa...")

        hasil = analisa_airdrop(pesan)

        notif = (
            "🤖 AGENT AIRDROP ALERT!\n\n"
            f"📢 Dari: {event.chat.title}\n\n"
            f"📝 Pesan:\n{pesan[:200]}...\n\n"
            f"🧠 Analisa AI:\n{hasil}"
        )

        await bot.send_message(chat_id=CHAT_ID, text=notif)

    await client.run_until_disconnected()

asyncio.run(main())
