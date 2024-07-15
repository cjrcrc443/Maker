from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from pyromod import listen



bot = Client(
    "mo",
    api_id="12962251",
    api_hash="b51499523800add51e4530c6f552dbc8",
    bot_token="6937321286:AAEh2B5dr2BFJBuRDa3Q5JKEoniXBOWfnic",
    plugins=dict(root="Maker")
    )

async def start_bot():
    print("[INFO]: STARTING BOT CLIENT")
    await bot.start()
    Alina = "Hawaallll"
    await bot.send_message(Alina, "**بە سەرکەوتوویی ڕێکخەری بۆت چالاکبوو 🥀،**")
    print("[INFO]: ڕێکخەر چالاکبوو و نامەکەم نارد بۆ گەشەپێدەر ⚡🚦.")
    await idle()
