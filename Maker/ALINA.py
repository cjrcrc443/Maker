import asyncio
import sys
from os import environ, execle

from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client
from pyrogram import Client as app
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import (
    ChatPrivileges,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
)

from ALINA.Data import db, dev, devname, get_data
from ALINA.info import Call, active, activecall, helper
from config import API_HASH, API_ID, MONGO_DB_URL, OWNER, OWNER_NAME, VIDEO, appp
from config import helper as ass
from config import user as usr

mongodb = _mongo_client_(MONGO_DB_URL)
mo = MongoClient()
mo = MongoClient(MONGO_DB_URL)
moo = mo["data"]
Bots = moo.alli
db = mongodb.db
botdb = db.botdb
blockdb = db.blocked


##########//((ئاماری ڕێکخەر)##########
async def data_user(client) -> list:
    data = await get_data(client)
    data = data.users
    list = []
    async for user in data.find({"user_id": {"$gt": 0}}):
        list.append(user)
    return list


##########//((ئاماری ڕێکخەر))##########
# Bots Run
Done = []
OFF = False


async def auto_bot():
    bots = Bots.find({})
    count = 0
    for i in bots:
        bot_username = i["bot_username"]
        try:
            if not i["bot_username"] in Done:
                TOKEN = i["token"]
                SESSION = i["session"]
                bot_username = i["bot_username"]
                devo = i["dev"]
                Done.append(bot_username)
                logger = i["logger"]
                bot = Client(
                    "ALINA",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    bot_token=TOKEN,
                    in_memory=True,
                    plugins=dict(root="ALINA"),
                )
                user = Client(
                    "ALINA",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    session_string=SESSION,
                    in_memory=True,
                )
                await bot.start()
                await user.start()
                appp[bot_username] = bot
                usr[bot_username] = user
                activecall[bot_username] = []
                dev[bot_username] = devo
                try:
                    devo = await bot.get_chat(devo)
                    devo = devo.first_name
                    devname[bot_username] = devo
                except:
                    devname[bot_username] = OWNER_NAME
                ass[bot_username] = []
                await helper(bot_username)
                await Call(bot_username)
                try:
                    await user.join_chat("Hawaall")
                except:
                    pass
                try:
                    await user.join_chat("ipceeoflifee7")
                except:
                    pass
                try:
                    await user.join_chat("pieceoflife00")
                except:
                    pass
                try:
                    await user.join_chat("aramii_dll")
                except:
                    pass
                try:
                    await user.join_chat("pieceofsad0")
                except:
                    pass
                try:
                    await user.join_chat("GroupAlina")
                except:
                    pass
                try:
                    await user.join_chat("EHS4SS")
                except:
                    pass
                try:
                    await user.join_chat("MGIMT")
                except:
                    pass
                try:
                    await user.join_chat("Haawall")
                except:
                    pass
        except Exception as e:
            print(f"[ @{bot_username} ] {e}")


# Bot Arledy Maked


async def restart_bot():
    args = [sys.executable, "main.py"]
    await execle(sys.executable, *args, environ)


async def get_served_bots() -> list:
    chats_list = []
    async for chat in botdb.find({"bot_username": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_bot(bot_username: int) -> bool:
    chat = await botdb.find_one({"bot_username": bot_username})
    if not chat:
        return False
    return True


async def add_served_bot(bot_username: int):
    is_served = await is_served_bot(bot_username)
    if is_served:
        return
    return await botdb.insert_one({"bot_username": bot_username})


async def del_served_bot(bot_username: int):
    is_served = await is_served_bot(bot_username)
    if not is_served:
        return
    return await botdb.delete_one({"bot_username": bot_username})


from pyrogram.errors import ChatAdminRequired, ChatWriteForbidden, UserNotParticipant

# join
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# --------------------------

MUST_JOIN = "Haawall"


# ------------------------
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://graph.org/file/c8d0d49f5e13290314807.jpg",
                    caption=f"**🧑🏻‍💻︙ببوورە ئەزیزم تۆ جۆین نیت؛\n🔰︙سەرەتا پێویستە جۆینی کەناڵی بۆت ♥️؛\n👾︙بکەیت بۆ بەکارهێنانم جۆین بە ⚜️؛\n💎︙کەناڵی بۆت: @Haawall\n\n👾︙کاتێ جۆینت کرد ستارت بکە /start , /help 📛!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("♥️ جۆینی کەناڵ بکە ♥️", url=link),
                            ]
                        ]
                    ),
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"**بۆت بکە ئەدمین لە کەناڵی**: {MUST_JOIN} !")


# Blocked User


async def get_block_users() -> list:
    chats_list = []
    async for chat in blockdb.find({"user_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_block_user(user_id: int) -> bool:
    chat = await blockdb.find_one({"user_id": user_id})
    if not chat:
        return False
    return True


async def add_block_user(user_id: int):
    is_served = await is_block_user(user_id)
    if is_served:
        return
    return await blockdb.insert_one({"user_id": user_id})


async def del_block_user(user_id: int):
    is_served = await is_block_user(user_id)
    if not is_served:
        return
    return await blockdb.delete_one({"user_id": user_id})


@app.on_message(filters.private)
async def botooott(client, message):
    try:
        if not message.chat.username in OWNER:
            if not message.from_user.id == client.me.id:
                await client.forward_messages(OWNER[0], message.chat.id, message.id)
    except Exception as e:
        pass
    message.continue_propagation()


@app.on_message(filters.command("چالاککردنی بۆتەکان", ""))
async def turnon(client, message):
    if message.chat.username in OWNER:
        m = await message.reply_text(
            "**♪ چالاککردنی هەموو بۆتەکان ..🚦⚡**", quote=True
        )
        try:
            await auto_bot()
        except:
            pass
        return await message.reply_text(
            "**◗⋮◖ هەموو بۆتەکان چالاککران 🚦⚡.**", quote=True
        )


@app.on_message(filters.command(["ناچالاککردنی ڕێکخەر", "چالاککردنی ڕێکخەر"], ""))
async def bye(client, message):
    user = message.from_user.username
    if user in OWNER:
        global OFF
        text = message.text
        if text == "چالاککردنی ڕێکخەر":
            OFF = None
            await message.reply_text("**♪ دۆخی بەخۆڕایی چالاککرا 🚦⚡.**", quote=True)
            return
        if text == "ناچالاککردنی ڕێکخەر":
            OFF = True
            await message.reply_text("**♪ دۆخی بەخۆڕایی ناچالاککرا 🚦⚡.**", quote=True)
            return


@app.on_message(filters.command("start") & filters.private)
async def stratmaked(client, message):
    if await is_block_user(message.from_user.id):
        return
    if OFF:
        if not message.chat.username in OWNER:
            return await message.reply_text(
                f"**👋🏻 ꒐ بۆت ناچالاککراوە \n👾 ꒐ نامە بۆ گەشەپێدەر بنێرە\n🧑🏻‍💻 ꒐ گەشەپێدەر : @{OWNER[0]}**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "˼  گەشەپێدەر  🧑🏻‍💻 ˹", url=f"https://t.me/{OWNER[0]}"
                            )
                        ]
                    ]
                ),
            )
    if message.chat.username in OWNER:
        kep = ReplyKeyboardMarkup(
            [
                ["دەرهێنانی کۆد", "نوێکردنەوەی ڕێکخەر"],
                ["دروستکردنی بۆت", "سڕینەوەی بۆت"],
                ["چالاککردنی ڕێکخەر", "ناچالاککردنی ڕێکخەر"],
                ["چالاککردنی بۆتەکان", "بۆتەکان"],
                ["پشکنینی بۆتەکان", "فلتەرکردنی بۆتەکان"],
                ["ئاماری بۆتەکان"],
                ["باندکردنی بۆت", "باندکردنی بەکارهێنەر"],
                ["لادانی باندی بۆت", "لادانی باندی بەکارهێنەر"],
                ["فۆرواردی گشتی", "ڕێکڵامی گشتی"],
                ["ئامارەکان"],
                ["فۆرواردی گەشەپێدەران", "چالاکی پەخش"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            f"**♪ بەخێربێی گەشەپێدەر 🚦⚡.**", reply_markup=kep, quote=True
        )
    else:
        kep = ReplyKeyboardMarkup(
            [
                ["• سڕینەوەی بۆت •", "• دروستکردنی بۆت •"],
                ["• سەرچاوە •", "• دەرهێنانی کۆد •"],
                ["• فێرکاری دروستکردن •"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            f"**👋🏻 ꒐ بەخێربێی {message.from_user.mention} ⚡.\n🤖 ꒐ بۆ ڕێکخەری بۆتی گۆرانی هەواڵ ⚡.**",
            reply_markup=kep,
            quote=True,
        )


@Client.on_message(filters.command(["/alive", "/source", "سەرچاوە", "• سەرچاوە •"], ""))
async def alive(client: Client, message):
    chat_id = message.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝗚𝗿𝗼𝘂𝗽 🖱️", url=f"https://t.me/pieceofsad0"),
                InlineKeyboardButton("𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🖱️", url=f"https://t.me/Haawall"),
            ],
            [InlineKeyboardButton(f"{OWNER_NAME}", url=f"https://t.me/{OWNER[0]}")],
        ]
    )
    alive = f"""**╭──── • ◈ • ────╮
么 [𝑺𝒐𝒖𝒓𝒄𝒆 𝑯𝒂𝒘𝒂𝒍](t.me/Haawall) 💎 .
么  [𝒅𝒆𝒗 𝑯𝒂𝒘𝒂𝒍](t.me/Hawaall) 💎 .
╰──── • ◈ • ────╯
🚦 𝚃𝙷𝙴 𝙱𝙴𝚂𝚃 𝚂𝙾𝚄𝚁𝙲𝙴 𝙾𝙽 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼  💎 .**"""

    await message.reply_photo(
        photo=VIDEO,
        caption=alive,
        reply_markup=keyboard,
    )


@app.on_message(filters.command("نوێکردنەوەی ڕێکخەر", ""))
async def update(client, message):
    msg = await message.reply_text(
        f"**♪ بە سەرکەوتوویی ڕێکخەر نوێکرایەوە 🚦⚡.**", quote=True
    )
    args = [sys.executable, "main.py"]
    await execle(sys.executable, *args, environ)


@Client.on_message(filters.command(["ئامارەکان"], ""))
async def user(client, message):
    if message.chat.username in OWNER:
        user = len(await data_user(client))
        return await message.reply_text(
            f"**♪ ژمارەی بەکارهێنەر ⟨ {user} ⟩ ئەندام 🚦⚡.**", quote=True
        )


@app.on_message(filters.command("چالاکی پەخش", ""))
async def activeee(client, message):
    nn = len(active)
    await message.reply_text(f"**♪ ژمارەی پەخشەکان {nn} 🚦⚡.**")


@app.on_message(filters.command(["• فێرکاری دروستکردن •", "فێرکاری دروستکردن"], ""))
async def createbot(client, message):
    await message.reply_text(
        "**👋🏻 ꒐ بەخێربێیت بۆ بەشی فێرکاری\n🤖 ꒐ لە ڕێگای ڤیدیۆوە فێری دروستکردنی بۆت بە\n💻 ꒐ بۆ بینینی ڤیدیۆ دووگمە دابگرە**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "فێرکاری دروستکردن", url=f"https://t.me/ferkaredrsutkrdnebot/6"
                    )
                ]
            ]
        ),
    )


@app.on_message(filters.command(["• دەرهێنانی کۆد •", "دەرهێنانی کۆد"], ""))
async def codev2(client, message):
    photo = "https://graph.org/file/5f052fa9418a10c5f9542.jpg"
    await message.reply_photo(
        photo,
        caption=f"**👋🏻 ꒐ {message.from_user.mention} بەخێربێیت بۆ بەشی کۆد\n🤖 ꒐ لە ڕێگای ئەم بۆت کۆد دەربهێنە\n🛡 ꒐ ئاگادربە تەنیا جۆری 𝗣𝘆𝗿𝗼𝗴𝗿𝗮𝗺 𝗩𝟮 بەکاردێت\n💻 ꒐ بۆت : @IQSGBOT دووگمە دابگرە**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "˹s ᴛ ʀ ɪ ɴ ɢ  ✗ s ᴇ s s ɪ ᴏ ɴ˼", url=f"https://t.me/IQSGBOT"
                    )
                ]
            ]
        ),
    )


OWNERdd = "474468585"


@app.on_message(filters.command(["دروستکردنی بۆت", "• دروستکردنی بۆت •"], ""))
async def cloner(app: Client, message):
    if await is_block_user(message.from_user.id):
        return

    # Check if the bot is currently disabled and if the sender is not the owner
    if OFF:
        if message.chat.username not in OWNER:
            await message.reply_text(
                f"**👋🏻 بۆت ناچالاککراوە\n👾 بۆ گەشەپێدەر بنێرە\n🧑🏻‍💻 گەشەپێدەر : @{OWNER[0]}**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "˼ گەشەپێدەر 🧑🏻‍💻 ˹", url=f"https://t.me/{OWNER[0]}"
                            )
                        ]
                    ]
                ),
            )
            return

    # Check if the command has the required number of arguments
    if len(message.command) < 3:
        await message.reply_text(
            "**• تۆکنی بۆت و کۆدی یاریدەدەر بنێرە بەتەرتیبی ئەمە:**\n`/دروستکردنی بۆت your_bot_token your_session_string`"
        )
        return

    # Get the bot token and session string from the command
    token = message.command[1]
    session = message.command[2]

    # Start the bot and check token validity
    try:
        await message.reply_text("**◗⋮◖ پشکنین بۆ تۆکنەکە دەکرێت ..⚡.**")
        bot = Client(
            "Cloner", api_id=API_ID, api_hash=API_HASH, bot_token=token, in_memory=True
        )
        await bot.start()
    except Exception:
        return await message.reply_text("**◗⋮◖ تۆکنی بۆت هەڵەیە 💎.**")

    # Check if bot is already served
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    if await is_served_bot(bot_username):
        await bot.stop()
        return await message.reply_text("**◗⋮◖ ناتوانی بۆت دروست بکەیت ⚡.**")
    if bot_username in Done:
        await bot.stop()
        return await message.reply_text("**◗⋮◖ پێشتر ئەم بۆتە دروستکراوە ⚡.**")

    # Initialize the user client with the provided session string
    user = Client(
        "ALINA",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session,
        in_memory=True,
    )
    try:
        await user.start()
    except Exception:
        await bot.stop()
        return await message.reply_text("**◗⋮◖ کۆدی یاریدەدەر هەڵەیە ⚡.**")

    # Create a supergroup for bot statistics and set permissions
    log_group = await user.create_supergroup(
        "گرووپی بۆت 🖤", "ئەم گرووپە هەموو ئامار و زانیاریەکانی بۆت سەیڤ دەکات"
    )
    if bot_info.photo:
        photo = await bot.download_media(bot_info.photo.big_file_id)
        await user.set_chat_photo(chat_id=log_group.id, photo=photo)
    await user.add_chat_members(log_group.id, bot_username)
    await user.promote_chat_member(
        log_group.id,
        bot_username,
        privileges=ChatPrivileges(
            can_change_info=True,
            can_invite_users=True,
            can_delete_messages=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=True,
            can_manage_chat=True,
            can_manage_video_chats=True,
        ),
    )

    # Save bot information to database
    log_group_link = await user.export_chat_invite_link(log_group.id)
    dev_id = (
        message.from_user.id
        if message.chat.username in OWNERdd
        else int((await app.ask(message.chat.id, "ئایدی خاوەنی بۆت بنێرە")).text)
    )
    Bots.insert_one(
        {
            "bot_username": bot_username,
            "token": token,
            "session": session,
            "dev": dev_id,
            "logger": log_group.id,
            "logger_mode": "ON",
        }
    )
    # Finalize and send confirmation messages
    await bot.stop()
    await user.stop()
    try:
        await auto_bot()
    except:
        pass
    await message.reply_text(
        f"**بە سەرکەوتوویی بۆتی گۆرانی دروستکرا 🚦⚡.\nگرووپی ئامار دروست کرا 🚦⚡.\n⟨ [{log_group_link}] ⟩**",
        disable_web_page_preview=True,
    )
    await app.send_message(
        OWNER[0], f"**◗⋮◖ بۆتی نوێ دروست کرا 🚦⚡.\nبۆت: @{bot_username}**"
    )


@app.on_message(filters.command(["سڕینەوەی بۆت", "• سڕینەوەی بۆت •"], ""))
async def delbot(client: app, message):
    if await is_block_user(message.from_user.id):
        return
    if OFF:
        if not message.chat.username in OWNER:
            return await message.reply_text(
                f"**👋🏻 ꒐ بۆت ناچالاککراوە \n👾 ꒐ نامە بۆ گەشەپێدەر بنێرە\n🧑🏻‍💻 ꒐ گەشەپێدەر : @{OWNER[0]}**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "˼  گەشەپێدەر  🧑🏻‍💻 ˹", url=f"https://t.me/{OWNER[0]}"
                            )
                        ]
                    ]
                ),
            )
    if message.chat.username in OWNER:
        ask = await client.ask(
            message.chat.id, "**◗⋮◖ یوزەری بۆت بنێرە 💎.**", timeout=200
        )
        bot_username = ask.text
        if "@" in bot_username:
            bot_username = bot_username.replace("@", "")
        list = []
        bots = Bots.find({})
        for i in bots:
            if i["bot_username"] == bot_username:
                botusername = i["bot_username"]
                list.append(botusername)
        if not bot_username in list:
            return await message.reply_text("**◗⋮◖ هیچ بۆتێکت دروست نەکردووە ⚡.**")
        else:
            try:
                bb = {"bot_username": bot_username}
                Bots.delete_one(bb)
                try:
                    Done.remove(bot_username)
                except:
                    pass
                try:
                    boot = appp[bot_username]
                    await boot.stop()
                except:
                    pass
                await message.reply_text("**◗⋮◖ بە سەرکەوتوویی بۆت سڕدرایەوە ⚡.**")
            except Exception as es:
                await message.reply_text(
                    f"**◗⋮◖ هەنێك هەڵە ڕوویدا ⚡.\n◗⋮◖ جۆری هەڵە :** `{es}` **⚡.**"
                )
    else:
        list = []
        bots = Bots.find({})
        for i in bots:
            try:
                if i["dev"] == message.chat.id:
                    bot_username = i["bot_username"]
                    list.append(i["dev"])
                    try:
                        Done.remove(bot_username)
                    except:
                        pass
                    try:
                        boot = appp[bot_username]
                        await boot.stop()
                        user = usr[bot_username]
                        await user.stop()
                    except:
                        pass
            except:
                pass
        if not message.chat.id in list:
            return await message.reply_text("**◗⋮◖ تۆ هێشتا بۆتت دروست نەکردووە 💎.**")
        else:
            try:
                dev = message.chat.id
                dev = {"dev": dev}
                Bots.delete_one(dev)
                await message.reply_text("**◗⋮◖ بە سەرکەوتوویی بۆتەکەت سڕدرایەوە ⚡.**")
            except:
                await message.reply_text(
                    "**◗⋮◖ هەنێك هەڵە هەیە نامە بۆ گەشەپێدەر بنێرە ⚡.\n◗⋮◖ گەشەپێدەر : @{OWNER[0]} ⚡.**"
                )


@app.on_message(filters.command("بۆتەکان", ""))
async def botsmaked(client, message):
    if message.chat.username in OWNER:
        m = 0
        text = ""
        bots = Bots.find({})
        try:
            for i in bots:
                try:
                    bot_username = i["bot_username"]
                    m += 1
                    user = i["dev"]
                    user = await client.get_users(user)
                    user = user.mention
                    text += f"♪ {m} -> @{bot_username} | By : {user}\n "
                except:
                    pass
        except:
            return await message.reply_text(
                "**♪ هیچ بۆتێکی دروستکراو بوونی نییە 🚦⚡.**"
            )
        try:
            await message.reply_text(
                f"**🤖 ꒐ ژمارەی بۆتە دروستکراوەکان : {m} .\n{text}**"
            )
        except:
            await message.reply_text("**♪ هیچ بۆتێکی دروستکراو بوونی نییە 🚦⚡.**")


async def get_users(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"user_id": {"$gt": 0}}):
        chats_list.append(chat)
    return chats_list


async def get_chats(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


@app.on_message(filters.command("ئاماری بۆتەکان", ""))
async def botstatus(client, message):
    if message.chat.username in OWNER:
        m = 0
        d = 0
        u = 0
        text = ""
        bots = Bots.find({})
        try:
            for i in bots:
                try:
                    bot_username = i["bot_username"]
                    database = mongodb[bot_username]
                    chatsdb = database.chats
                    chat = len(await get_chats(chatsdb))
                    m += chat
                    chatsdb = database.users
                    chat = len(await get_users(chatsdb))
                    u += chat
                    d += 1
                except Exception as e:
                    print(e)
        except:
            return await message.reply_text(
                "**♪ هیچ بۆتێکی دروستکراو بوونی نییە 🚦⚡.**"
            )
        try:
            await message.reply_text(
                f"**🤖 ꒐ بۆتە دروستکراوەکان {d} .\n💎 ꒐ ژمارەی گرووپەکان {m} .\n🖲 ꒐ ژمارەی بەکارهێنەر {u} .**"
            )
        except:
            await message.reply_text("**♪ هیچ بۆتێکی دروستکراو بوونی نییە 🚦⚡.**")


@app.on_message(
    filters.command(
        [
            "باندکردنی بۆت",
            "باندکردنی بەکارهێنەر",
            "لادانی باندی بۆت",
            "لادانی باندی بەکارهێنەر",
        ],
        "",
    )
)
async def blockk(client: app, message):
    if message.chat.username in OWNER:
        ask = await client.ask(message.chat.id, "**♪ یوزەری بنێرە 🚦⚡.**", timeout=200)
        if ask.text == "هەڵوەشاندنەوە":
            return await ask.reply_text("**♪ بە سەرکەوتوویی هەڵوەشێنرایەوە 🚦⚡.**")
        i = ask.text
        if "@" in i:
            i = i.replace("@", "")
        if (
            message.command[0] == "باندکردنی بۆت"
            or message.command[0] == "لادانی باندی بۆت"
        ):
            bot_username = i
            if await is_served_bot(bot_username):
                if message.command[0] == "لادانی باندی بۆت":
                    await del_served_bot(bot_username)
                    return await ask.reply_text(
                        "**♪ بە سەرکەوتوویی بۆت باندی لادرا 🚦⚡.**"
                    )
                else:
                    return await ask.reply_text("**♪ پێشتر باندکراوە 🚦⚡.**")
            else:
                if message.command[0] == "لادانی باندی بۆت":
                    return await ask.reply_text("**♪ پێشتر باندکراوە 🚦⚡.**")
                await add_served_bot(bot_username)
                try:
                    Done.remove(bot_username)
                    boot = appp[bot_username]
                    await boot.stop()
                    user = usr[bot_username]
                    await user.stop()
                except:
                    pass
                return await ask.reply_text("**♪ بە سەرکەوتوویی بۆت باندکرا 🚦⚡.**")
        else:
            user_id = int(i)
            if await is_block_user(user_id):
                if message.command[0] == "لادانی باندی بەکارهێنەر":
                    await del_block_user(bot_username)
                    return await ask.reply_text(
                        "**♪ بە سەرکەوتوویی بەکارهێنەر باندی لادرا 🚦⚡.**"
                    )
                return await ask.reply_text("**♪ پێشتر باندکراوە 🚦⚡.**")
            else:
                if message.command[0] == "لادانی باندی بەکارهێنەر":
                    return await ask.reply_text("**♪ پێشتر باندکراوە 🚦⚡.**")
                await add_block_user(user_id)
                return await ask.reply_text(
                    "**♪ بە سەرکەوتوویی بەکارهێنەر باندکرا 🚦⚡.**"
                )


@app.on_message(filters.command(["فۆرواردی گشتی", "ڕێکڵامی گشتی"], ""))
async def casttoall(client: app, message):
    if message.chat.username in OWNER:
        sss = "ڕێکڵام" if message.command[0] == "ڕێکڵامی گشتی" else "فۆروارد"
        ask = await client.ask(message.chat.id, f"**بنێرە {sss} **", timeout=200)
        x = ask.id
        y = message.chat.id
        if ask.text == "هەڵوەشاندنەوە":
            return await ask.reply_text("**♪ بە سەرکەوتوویی هەڵوەشێنرایەوە 🚦⚡.**")
        pn = await client.ask(
            message.chat.id,
            "**دەتەوێت نامەکە پین بکەم ؟\nبنێرە « بەڵێ » یان « نەخێر »**",
            timeout=200,
        )
        h = await message.reply_text("**♪ کەمێك چاوەڕێ بکە کات دەخایەنێ 🚦⚡.**")
        b = 0
        s = 0
        c = 0
        u = 0
        sc = 0
        su = 0
        bots = Bots.find({})
        for bott in bots:
            try:
                b += 1
                s += 1
                bot_username = bott["bot_username"]
                session = bott["session"]
                bot = appp[bot_username]
                user = usr[bot_username]
                db = mongodb[bot_username]
                chatsdb = db.chats
                chats = await get_chats(chatsdb)
                usersdb = db.users
                users = await get_users(usersdb)
                all = []
                for i in users:
                    all.append(int(i["user_id"]))
                for i in chats:
                    all.append(int(i["chat_id"]))
                for i in all:
                    if message.command[0] == "ڕێکڵامی گشتی":
                        try:
                            m = await bot.forward_messages(i, y, x)
                            if m.chat.type == ChatType.PRIVATE:
                                u += 1
                            else:
                                c += 1
                            if pn.text == "بەڵێ":
                                try:
                                    await m.pin(disable_notification=False)
                                except:
                                    continue
                        except FloodWait as e:
                            flood_time = int(e.value)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
                    else:
                        try:
                            m = await bot.send_message(chat_id=i, text=ask.text)
                            if m.chat.type == ChatType.PRIVATE:
                                u += 1
                            else:
                                c += 1
                            if pn.text == "بەڵێ":
                                await m.pin(disable_notification=False)
                        except FloodWait as e:
                            flood_time = int(e.value)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
                async for i in user.get_dialogs():
                    chat_id = i.chat.id
                    if message.command[0] == "فۆرواردی گشتی":
                        try:
                            m = await user.forward_messages(i, y, x)
                            if m.chat.type == ChatType.PRIVATE:
                                su += 1
                            else:
                                sc += 1
                            if pn.text == "بەڵێ":
                                await m.pin(disable_notification=False)
                        except FloodWait as e:
                            flood_time = int(e.value)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
                    else:
                        try:
                            m = await user.send_message(chat_id, ask.text)
                            if m.chat.type == ChatType.PRIVATE:
                                su += 1
                            else:
                                sc += 1
                            if pn.text == "بەڵێ":
                                await m.pin(disable_notification=False)
                        except FloodWait as e:
                            flood_time = int(e.x)
                            if flood_time > 200:
                                continue
                            await asyncio.sleep(flood_time)
                        except Exception as e:
                            continue
            except Exception as es:
                print(es)
                await message.reply_text(es)
        try:
            await message.reply_text(
                f"**بەسەرکەوتووی نێردرا**\n**نێردرا بە بەکارهێنانی {b} بۆت**\n**بۆ {c} گرووپ و {u} بەکارهێنەر**\n**نێردرا بە بکارهێنانی {s} یاریدەدەر**\n**بۆ {sc} گرووپ و {su} بەکارهێنەر**"
            )
        except Exception as es:
            await message.reply_text(es)


@app.on_message(filters.command(["فۆرواردی گەشەپێدەران"], ""))
async def cast_dev(client, message):
    if message.chat.username in OWNER:
        ask = await client.ask(
            message.chat.id, "**♪ نامەکەت بنێرە 🚦⚡.**", timeout=300
        )
        if ask.text == "هەڵوەشاندنەوە":
            return await ask.reply_text("هەڵوەشاندنەوە")
        d = 0
        f = 0
        bots = Bots.find({})
        for i in bots:
            try:
                dev = i["dev"]
                bot_username = i["bot_username"]
                bot = appp[bot_username]
                try:
                    await bot.send_message(dev, ask.text)
                    d += 1
                except Exception as es:
                    print(es)
                    f += 1
            except Exception:
                f += 1
        return await ask.reply_text(
            f"**♪ ناردم بۆ {d} گەشەپێدەر 🚦⚡.\n♪ شکستی هێنا لە {f} گەشەپێدەر 🚦⚡.**"
        )


@app.on_message(filters.command(["پشکنینی بۆتەکان"], ""))
async def testbots(client, message):
    if message.chat.username in OWNER:
        bots = Bots.find({})
        text = "**💻 ꒐ ئاماری بۆتەکان**\n"
        b = 0
        for i in bots:
            try:
                bot_username = i["bot_username"]
                database = mongodb[bot_username]
                chatsdb = database.chats
                g = len(await get_chats(chatsdb))
                b += 1
                text += f"\n**{b} -> @{bot_username} | Group : {g}**"
            except Exception as es:
                print(es)
        await message.reply_text(text)


@app.on_message(filters.command(["فلتەرکردنی بۆتەکان"], ""))
async def checkbot(client: app, message):
    if message.chat.username in OWNER:
        ask = await client.ask(
            message.chat.id, "**♪ کەمترین ئامار پێشکەش بکە 🚦⚡.**", timeout=30
        )
        if ask.text == "هەڵوەشاندنەوە":
            return await ask.reply_text(
                "**♪ بە سەرکەوتوویی هەڵوەشێنرایەوە 🚦⚡.**", quote=True
            )
        bots = Bots.find({})
        m = ask.text
        m = int(m)
        text = f"**♪ ئەم بۆتانە ڕاگیراون چونکە ئامارەکان کەمترن لە... : {ask.text} گرووپ 🚦⚡.**"
        b = 0
        for i in bots:
            try:
                bot_username = i["bot_username"]
                database = mongodb[bot_username]
                chatsdb = database.chats
                g = len(await get_chats(chatsdb))
                if g < m:
                    b += 1
                    boot = appp[bot_username]
                    await boot.stop()
                    ii = {"bot_username": bot_username}
                    Bots.delete_one(ii)
                    try:
                        Done.remove(bot_username)
                    except:
                        pass
                    try:
                        boot = appp[bot_username]
                        await boot.stop()
                        user = usr[bot_username]
                        await user.stop()
                    except:
                        pass
                    text += f"\n**{b} -> @{bot_username} | Group : {g}**"
            except Exception as es:
                print(es)
        await message.reply_text(text)


import asyncio
from datetime import datetime
from os import system as execute

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import Client, filters
from urllib3 import disable_warnings, exceptions

UPSTREAM_BRANCH = "main"
GIT_TOKEN = ""
UPSTREAM_REPO = "https://github.com/cjrcrc443/Maker"

disable_warnings(exceptions.InsecureRequestWarning)


@app.on_message(
    filters.command(["update", "gitpull", "up"]) & filters.user(OWNER) & filters.private
)
async def update_(client: Client, message):
    response = await message.reply_text("Checking for available updates....")

    repo_link = UPSTREAM_REPO
    if GIT_TOKEN:
        git_username = repo_link.split("com/")[1].split("/")[0]
        temp_repo = repo_link.split("https://")[1]
        repo_link = f"https://{git_username}:{GIT_TOKEN}@{temp_repo}"

    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("origin", repo_link)
        origin.fetch()
        repo.create_head(UPSTREAM_BRANCH, origin.refs[UPSTREAM_BRANCH])
        repo.heads[UPSTREAM_BRANCH].set_tracking_branch(origin.refs[UPSTREAM_BRANCH])
        repo.heads[UPSTREAM_BRANCH].checkout()
    except GitCommandError:
        return await response.edit("Git command error occurred.")

    repo.remote("origin").fetch(UPSTREAM_BRANCH)
    execute(f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(7)

    update_count = sum(1 for _ in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"))

    if not update_count:
        return await response.edit("» Bot is up-to-date.")

    ordinal = lambda n: f"{n}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"

    updates = "".join(
        f"<b>➣ #{info.count()}: <a href={repo.remotes.origin.url}/commit/{info}>{info.summary}</a> "
        f"By -> {info.author}</b>\n<b>➥ Commited On :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} "
        f"{datetime.fromtimestamp(info.committed_date).strftime('%b, %Y')}\n\n"
        for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}")
    )

    if len(updates) > 4096:
        url = await Alinabin(updates)
        await response.edit(
            f"**A new update is available for the bot**\n\n[Check Updates]({url})",
            disable_web_page_preview=True,
        )
    else:
        await response.edit(
            f"**A new update is available for the bot**\n\n{updates}",
            disable_web_page_preview=True,
        )

    execute("git stash &> /dev/null && git pull")
    await restart_bot()
