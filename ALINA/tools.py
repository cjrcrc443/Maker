import asyncio
from datetime import datetime

import aiohttp
from pyrogram import Client, enums, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message, ReplyKeyboardMarkup

from ALINA.Data import Bots, get_dev, get_userbot
from ALINA.info import (
    activecall,
    del_served_chat,
    del_served_user,
    get_served_chats,
    get_served_users,
)
from config import OWNER
from config import logger as log
from config import logger_mode as logm

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def base(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link


@Client.on_message(filters.command(["• ئامارەکان •", "ئامارەکان"], ""))
async def analysis(client: Client, message: Message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        chats = len(await get_served_chats(client))
        user = len(await get_served_users(client))
        return await message.reply_text(
            f"**✅ ئامارەکانی بۆت**\n**⚡ گرووپەکان {chats} گرووپ**\n**⚡ بەکارهێنەرەکان {user} بەکارهێنەر**"
        )


@Client.on_message(filters.command(["• گرووپەکان •", "گرووپەکان"], ""))
async def chats_func(client: Client, message: Message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        m = await message.reply_text("⚡")
        served_chats = []
        text = ""
        chats = await get_served_chats(client)
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
        count = 0
        co = 0
        msg = ""
        for served_chat in served_chats:
            if f"{served_chat}" in text:
                await del_served_chat(client, served_chat)
            else:
                try:
                    chat = await client.get_chat(served_chat)
                    title = chat.title
                    username = chat.username
                    count += 1
                    txt = (
                        f"{count}:- گرووپ : [{title}](https://t.me/{username}) ئایدی : `{served_chat}`\n"
                        if username
                        else f"{count}:- گرووپ : {title} ئایدی : `{served_chat}`\n"
                    )
                    text += txt
                except Exception:
                    title = "Not Found"
                    count += 1
                    text += f"{count}:- {title} {served_chat}\n"
        if count == 0:
            return await m.edit("ئامارەکان بەتاڵە 🤔")
        else:
            try:
                await message.reply_text(text, disable_web_page_preview=True)
            except:
                link = await base(text)
                await message.reply_text(link)
            return await m.delete()


@Client.on_message(filters.command(["• بەکارهێنەرەکان •", "بەکارهێنەرەکان"], ""))
async def users_func(client: Client, message: Message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        m = await message.reply_text("⚡")
        served_chats = []
        text = ""
        chats = await get_served_users(client)
        for chat in chats:
            served_chats.append(int(chat["user_id"]))
        count = 0
        co = 0
        msg = ""
        for served_chat in served_chats:
            if f"{served_chat}" in text:
                await del_served_user(client, served_chat)
            else:
                try:
                    chat = await client.get_chat(served_chat)
                    title = chat.first_name
                    username = chat.username
                    count += 1
                    txt = (
                        f"{count} :- گرووپ : [{title}](https://t.me/{username}) ئایدی : `{served_chat}`\n"
                        if username
                        else f"{count}:- گرووپ : {title} ئایدی : `{served_chat}`\n"
                    )
                    text += txt
                except Exception:
                    title = "Not Found"
                    count += 1
                    text += f"{count}:- {title} {served_chat}\n"
        if count == 0:
            return await m.edit("ئامارەکان بەتاڵە 🤔")
        else:
            try:
                await message.reply_text(text, disable_web_page_preview=True)
            except:
                link = await base(text)
                await message.reply_text(link)
            return await m.delete()


@Client.on_message(filters.command(["• تێلی چالاك •", "تێلی چالاك"], ""))
async def geetmeactive(client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        m = await message.reply_text("**هێنانی تێلە چالاکەکان ..🚦**")
        count = 0
        text = ""
        for i in activecall[client.me.username]:
            try:
                chat = await client.get_chat(i)
                count += 1
                text += (
                    f"{count}- [{chat.title}](https://t.me/{chat.username}) : {chat.id}"
                    if chat.username
                    else f"{chat.title} : {chat.id}"
                )
            except Exception:
                title = "Not Found"
                count += 1
                text += f"{count}:- {title} {chat.id}\n"
        if count == 0:
            return await m.edit("**هیچ تێلێکی چالاك بوونی نییە 🤔**")
        else:
            try:
                await message.reply_text(text, disable_web_page_preview=True)
            except:
                link = await base(text)
                await message.reply_text(link)
            return await m.delete()


@Client.on_message(
    filters.command(["• بەشی فۆروارد •", "• گەڕانەوە •", "بەشی فۆروارد"], "")
)
async def cast(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        kep = ReplyKeyboardMarkup(
            [
                ["• فۆرواردی گشتی •"],
                ["• فۆروارد بۆ گرووپەکان •", "• فۆروارد بۆ بەکارهێنەرەکان •"],
                ["• ڕێکڵامی گشتی •"],
                ["• ڕێکڵام بۆ گرووپەکان •", "• ڕێکڵام بۆ بەکارهێنەرەکان •"],
                ["• گەڕانەوە بۆ لیستی سەرەکی •"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            "**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی فۆروارد**",
            reply_markup=kep,
        )


@Client.on_message(
    filters.command(
        [
            "• فۆرواردی گشتی •",
            "• فۆروارد بۆ گرووپەکان •",
            "• فۆروارد بۆ بەکارهێنەرەکان •",
            "• ڕێکڵامی گشتی •",
            "• ڕێکڵام بۆ بەکارهێنەرەکان •",
            "• ڕێکڵام بۆ گرووپەکان •",
        ],
        "",
    )
)
async def cast1(client: Client, message):
    command = message.command[0]
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        if command == "• فۆرواردی گشتی •":
            kep = ReplyKeyboardMarkup(
                [
                    ["• فۆرواردی گشتی بە بۆت •"],
                    ["• فۆرواردی گشتی بە یاریدەدەر •"],
                    ["• گەڕانەوە •"],
                ],
                resize_keyboard=True,
            )
            await message.reply_text(
                "**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی فۆروارد**",
                reply_markup=kep,
            )
        elif command == "• فۆروارد بۆ گرووپەکان •":
            kep = ReplyKeyboardMarkup(
                [
                    ["• فۆروارد بۆ گرووپەکان بە بۆت •"],
                    ["• فۆروارد بۆ گرووپەکان بە یاریدەدەر •"],
                    ["• گەڕانەوە •"],
                ],
                resize_keyboard=True,
            )
            await message.reply_text(
                "**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی فۆروارد**",
                reply_markup=kep,
            )
        elif command == "• فۆروارد بۆ بەکارهێنەرەکان •":
            kep = ReplyKeyboardMarkup(
                [
                    ["• فۆروارد بۆ بەکارهێنەرەکان بە بۆت •"],
                    ["• فۆروارد بۆ بەکارهێنەرەکان بە یاریدەدەر •"],
                    ["• گەڕانەوە •"],
                ],
                resize_keyboard=True,
            )
            await message.reply_text(
                "**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی فۆروارد**",
                reply_markup=kep,
            )
        elif command == "• ڕێکڵامی گشتی •":
            kep = ReplyKeyboardMarkup(
                [["• ڕێکڵامی گشتی بە بۆت •"], ["• گەڕانەوە •"]], resize_keyboard=True
            )
            await message.reply_text(
                "**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی فۆروارد**",
                reply_markup=kep,
            )
        elif command == "• ڕێکڵام بۆ بەکارهێنەرەکان •":
            kep = ReplyKeyboardMarkup(
                [["• ڕێکڵام بۆ بەکارهێنەرەکان بە بۆت •"], ["• گەڕانەوە •"]],
                resize_keyboard=True,
            )
            await message.reply_text(
                "**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی فۆروارد**",
                reply_markup=kep,
            )
        else:
            kep = ReplyKeyboardMarkup(
                [["• ڕێکڵام بۆ گرووپەکان بە بۆت •"], ["• گەڕانەوە •"]],
                resize_keyboard=True,
            )
            await message.reply_text(
                "**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی فۆروارد**",
                reply_markup=kep,
            )


@Client.on_message(
    filters.command(
        [
            "• فۆرواردی گشتی بە یاریدەدەر •",
            "• فۆرواردی گشتی بە بۆت •",
            "• فۆروارد بۆ گرووپەکان بە یاریدەدەر •",
            "• فۆروارد بۆ گرووپەکان بە بۆت •",
            "• فۆروارد بۆ بەکارهێنەرەکان بە یاریدەدەر •",
            "• فۆروارد بۆ بەکارهێنەرەکان بە بۆت •",
            "• ڕێکڵامی گشتی بە یاریدەدەر •",
            "• ڕێکڵامی گشتی بە بۆت •",
            "• ڕێکڵام بۆ گرووپەکان بە یاریدەدەر •",
            "• ڕێکڵام بۆ گرووپەکان بە بۆت •",
            "• ڕێکڵام بۆ بەکارهێنەرەکان بە یاریدەدەر •",
            "• ڕێکڵام بۆ بەکارهێنەرەکان بە بۆت •",
        ],
        "",
    )
)
async def cast5(client: Client, message):
    command = message.command[0]
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        kep = ReplyKeyboardMarkup(
            [["• هەڵوەشاندنەوە •"], ["• گەڕانەوە •"], ["• گەڕانەوە بۆ لیستی سەرەکی •"]],
            resize_keyboard=True,
        )
        ask = await client.ask(
            message.chat.id,
            "**ئێستا ئەو شتە بنێرە کە دەتەوێت بینێرم ⚡.**",
            reply_markup=kep,
        )
        x = ask.id
        y = message.chat.id
        if ask.text == "• هەڵوەشاندنەوە •":
            return await ask.reply_text("**♪ بە سەرکەوتوویی هەڵوەشێنرایەوە 🚦⚡.**")
        pn = await client.ask(
            message.chat.id,
            "**دەتەوێت نامەکە پین بکەم ؟\nبنێرە « بەڵێ » یان « نەخێر »**",
        )
        await message.reply_text("**فۆرواردی نامەکەت دەکەم چاوەڕێ بکە ..⚡**")
        text = ask.text
        dn = 0
        fd = 0
        if command == "• فۆرواردی گشتی بە بۆت •":
            chats = await get_served_chats(client)
            users = await get_served_users(client)
            chat = []
            for user in users:
                chat.append(int(user["user_id"]))
            for c in chats:
                chat.append(int(c["chat_id"]))
            for i in chat:
                try:
                    m = await client.send_message(chat_id=i, text=text)
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• فۆرواردی گشتی بە یاریدەدەر •":
            user = await get_userbot(bot_username)
            async for i in user.get_dialogs():
                try:
                    m = await user.send_message(chat_id=i.chat.id, text=text)
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• فۆروارد بۆ گرووپەکان بە بۆت •":
            chats = await get_served_chats(client)
            chat = []
            for c in chats:
                chat.append(int(c["chat_id"]))
            for i in chat:
                try:
                    m = await client.send_message(chat_id=i, text=text)
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• فۆروارد بۆ گرووپەکان بە یاریدەدەر •":
            user = await get_userbot(bot_username)
            async for i in user.get_dialogs():
                if not i.chat.type == enums.ChatType.PRIVATE:
                    try:
                        m = await user.send_message(chat_id=i.chat.id, text=text)
                        dn += 1
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
                        fd += 1
                        continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• فۆروارد بۆ بەکارهێنەرەکان بە بۆت •":
            chats = await get_served_users(client)
            chat = []
            for c in chats:
                chat.append(int(c["user_id"]))
            for i in chat:
                try:
                    i = i
                    m = await client.send_message(chat_id=i, text=text)
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• فۆروارد بۆ بەکارهێنەرەکان بە یاریدەدەر •":
            client = await get_userbot(bot_username)
            async for i in client.get_dialogs():
                if i.chat.type == enums.ChatType.PRIVATE:
                    try:
                        m = await client.send_message(chat_id=i.chat.id, text=text)
                        dn += 1
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
                        fd += 1
                        continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• ڕێکڵامی گشتی بە بۆت •":
            chats = await get_served_chats(client)
            users = await get_served_users(client)
            chat = []
            for user in users:
                chat.append(int(user["user_id"]))
            for c in chats:
                chat.append(int(c["chat_id"]))
            for i in chat:
                try:
                    m = await client.forward_messages(i, y, x)
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• ڕێکڵامی گشتی بە یاریدەدەر •":
            client = await get_userbot(bot_username)
            async for i in client.get_dialogs():
                try:
                    m = await client.forward_messages(
                        chat_id=i.chat.id,
                        from_chat_id=message.chat.username,
                        message_ids=int(x),
                    )
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• ڕێکڵام بۆ گرووپەکان بە بۆت •":
            chats = await get_served_chats(client)
            chat = []
            for user in chats:
                chat.append(int(user["chat_id"]))
            for i in chat:
                try:
                    m = await client.forward_messages(i, y, x)
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• ڕێکڵام بۆ گرووپەکان بە یاریدەدەر •":
            client = await get_userbot(bot_username)
            async for i in client.get_dialogs():
                if not i.chat.type == enums.ChatType.PRIVATE:
                    try:
                        m = await client.forward_messages(i.chat.id, y, x)
                        dn += 1
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
                        fd += 1
                        continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• ڕێکڵام بۆ بەکارهێنەرەکان بە بۆت •":
            chats = await get_served_users(client)
            chat = []
            for c in chats:
                chat.append(int(c["user_id"]))
            for i in chat:
                try:
                    m = await client.forward_messages(i, y, x)
                    dn += 1
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
                    fd += 1
                    continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )
        elif command == "• ڕێکڵام بۆ بەکارهێنەرەکان بە یاریدەدەر •":
            client = await get_userbot(bot_username)
            async for i in client.get_dialogs():
                if i.chat.type == enums.ChatType.PRIVATE:
                    try:
                        m = await client.forward_messages(i.chat.id, y, x)
                        dn += 1
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
                    except:
                        fd += 1
                        continue
            return await message.reply_text(
                f"**بە سەرکەوتوویی فۆروارد کرا ⚡**\n\n**بۆ : {dn}**\n**شکستی هێنا لە : {fd}**"
            )


# کۆنتڕۆڵی یریدەدەر


@Client.on_message(
    filters.command(["• بەشی ئەکاونتی یاریدەدەر •", "بەشی ئەکاونتی یاریدەدەر"], "")
)
async def helpercn(client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    userbot = await get_userbot(bot_username)
    me = userbot.me
    i = f"@{me.username} : {me.id}" if me.username else me.id
    b = await client.get_chat(me.id)
    b = b.bio if b.bio else "**بایۆی نییە**"
    if message.chat.id == dev or message.chat.username in OWNER:
        kep = ReplyKeyboardMarkup(
            [
                ["• پشکنینی یاریدەدەر •"],
                ["• گۆڕینی ناوی یەکەم •", "• گۆڕینی ناوی دووەم •"],
                ["• گۆڕینی بایۆ •"],
                ["• گۆڕینی یوزەری یاریدەدەر •"],
                ["• گۆڕینی وێنە •", "• لادانی وێنە •"],
                ["• بانگکردنی یاریدەدەر •"],
                ["• گەڕانەوە بۆ لیستی سەرەکی •"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            f"**👋🏻 ꒐ بەخێربێی گەشەپێدەری ئەزیز **\n**⚡ ꒐ بۆ بەشی ئەکاونتی یاریدەدەر**\n**{me.mention}**\n**{i}**\n**{b}**",
            reply_markup=kep,
        )


@Client.on_message(filters.command(["پشکنینی یاریدەدەر •", "پشکنینی یاریدەدەر •"], ""))
async def userrrrr(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        client = await get_userbot(bot_username)
        mm = await message.reply_text("Collecting stats")
        start = datetime.now()
        u = 0
        g = 0
        sg = 0
        c = 0
        b = 0
        a_chat = 0
        Meh = client.me
        usere = Meh.mention
        async for dialog in client.get_dialogs():
            type = dialog.chat.type
            if enums.ChatType.PRIVATE == type:
                u += 1
            elif enums.ChatType.BOT == type:
                b += 1
            elif enums.ChatType.GROUP == type:
                g += 1
            elif enums.ChatType.SUPERGROUP == type:
                sg += 1
                user_s = await dialog.chat.get_member(int(Meh.id))
                if (
                    user_s.status == enums.ChatMemberStatus.ADMINISTRATOR
                    or user_s.status == enums.ChatMemberStatus.OWNER
                ):
                    a_chat += 1
            elif enums.ChatType.CHANNEL == type:
                c += 1
            else:
                print(type)

        end = datetime.now()
        ms = (end - start).seconds
        await mm.edit_text(
            """**ꜱᴛᴀᴛꜱ ꜰᴇᴀᴛᴄʜᴇᴅ ɪɴ {} ꜱᴇᴄᴏɴᴅꜱ ⚡**
⚡**ʏᴏᴜ ʜᴀᴠᴇ {} ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ɢʀᴏᴜᴘꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ꜱᴜᴘᴇʀ ɢʀᴏᴜᴘꜱ.**
🏷️**ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ {} ᴄʜᴀɴɴᴇʟꜱ.**
🏷️**ʏᴏᴜ ᴀʀᴇ ᴀᴅᴍɪɴꜱ ɪɴ {} ᴄʜᴀᴛꜱ.**
🏷️**ʙᴏᴛꜱ ɪɴ ʏᴏᴜʀ ᴘʀɪᴠᴀᴛᴇ = {}**
⚠️**ꜰᴇᴀᴛᴄʜᴇᴅ ʙʏ ᴜꜱɪɴɢ {} **""".format(
                ms, u, g, sg, c, a_chat, b, usere
            )
        )


@Client.on_message(filters.command(["• گۆڕینی ناوی یەکەم •", "گۆڕینی ناوی یەکەم"], ""))
async def changefisrt(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        try:
            name = await client.ask(message.chat.id, "**• ئێستا ناوە نوێیەکە بنێرە •**")
            name = name.text
            client = await get_userbot(bot_username)
            await client.update_profile(first_name=name)
            await message.reply_text(
                "**بە سەرکەوتوویی ناوی ئەکاونتی یاریدەدەر گۆڕا ⚡.**"
            )
        except Exception as es:
            await message.reply_text(f"**• هەڵە ڕوویدا لە گۆڕینی ناو\n {es} **")


@Client.on_message(filters.command(["• گۆڕینی ناوی دووەم •", "گۆڕینی ناوی دووەم"], ""))
async def changelast(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        try:
            name = await client.ask(message.chat.id, "**• ئێستا ناوە نوێیەکە بنێرە •**")
            name = name.text
            client = await get_userbot(bot_username)
            await client.update_profile(last_name=name)
            await message.reply_text(
                "**بە سەرکەوتوویی ناوی ئەکاونتی یاریدەدەر گۆڕا ⚡.**"
            )
        except Exception as es:
            await message.reply_text(f"**• هەڵە ڕوویدا لە گۆڕینی ناو\n {es} **")


@Client.on_message(filters.command(["• گۆڕینی بایۆ •", "گۆڕینی بایۆ"], ""))
async def changebio(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        try:
            name = await client.ask(message.chat.id, "**• ئێستا بایۆی نوێ بنێرە •**")
            name = name.text
            client = await get_userbot(bot_username)
            await client.update_profile(bio=name)
            await message.reply_text("**بە سەرکەوتوویی بایۆ گۆڕا ⚡.**")
        except Exception as es:
            await message.reply_text(f"**• هەڵە ڕوویدا لە گۆڕینی بایۆ\n {es} **")


@Client.on_message(
    filters.command(["• گۆڕینی یوزەری یاریدەدەر •", "گۆڕینی یوزەری یاریدەدەر"], "")
)
async def changeusername(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        try:
            name = await client.ask(
                message.chat.id, "**• ئێستا یوزەرە نوێیەکە بنێرە •**"
            )
            name = name.text
            client = await get_userbot(bot_username)
            await client.set_username(name)
            await message.reply_text("**بە سەرکەوتوویی یوزەری یاریدەدەر گۆڕا ⚡.**")
        except Exception as es:
            await message.reply_text(
                f"**• هەڵە ڕوویدا لە گۆڕینی یوزەری یاریدەدەر\n {es} **"
            )


@Client.on_message(filters.command(["• گۆڕینی وێنە •", "گۆڕینی وێنە"], ""))
async def changephoto(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        try:
            m = await client.ask(message.chat.id, "**• ئێستا وێنە نوێیەکە بنێرە •**")
            photo = await m.download()
            client = await get_userbot(bot_username)
            await client.set_profile_photo(photo=photo)
            await message.reply_text(
                "***بە سەرکەوتوویی وێنەی ئەکاونتی یاریدەدەر گۆڕا ⚡.**"
            )
        except Exception as es:
            await message.reply_text(f"**• هەڵە ڕوویدا لە گۆڕینی وێنە\n {es} **")


@Client.on_message(filters.command(["اضافه صوره"], ""), group=5865067)
async def changephoto(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    user = await get_userbot(bot_username)
    if message.chat.id == dev or message.chat.username in caes:
        try:
            m = await client.ask(message.chat.id, "قم بإرسال الصوره الجديده الان")
            photo = m.photo
            photo = await client.download_media(photo)
            await user.set_profile_photo(photo=photo)
            await message.reply_text("تم تغير صوره الحساب المساعد بنجاح ..")
        except Exception as es:
            await message.reply_text(f" حدث خطأ أثناء تغير الصوره \n {es}")


@Client.on_message(filters.command(["• لادانی وێنە •", "لادانی وێنە"], ""))
async def changephotos(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        try:
            client = await get_userbot(bot_username)
            photos = await client.get_profile_photos("me")
            await client.delete_profile_photos([p.file_id for p in photos[1:]])
            await message.reply_text("**بە سەرکەوتوویی وێنە لادرا ⚡.**")
        except Exception as es:
            await message.reply_text(f"**• هەڵە ڕوویدا لە لادانی وێنە\n {es} **")


@Client.on_message(filters.command("• بانگکردنی یاریدەدەر •", ""))
async def joined(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        try:
            name = await client.ask(message.chat.id, "**• لینکی گرووپ بنێرە •**")
            name = name.text
            if "https" in name:
                if not "+" in name:
                    name = name.replace("https://t.me/", "")
            client = await get_userbot(bot_username)
            await client.join_chat(name)
            await message.reply_text(
                "**بە سەرکەوتوویی ئەکاونی یاریدەدەر جۆینی کرد ⚡**"
            )
        except Exception as es:
            await message.reply_text(f"** هەڵە ڕوویدا لە کاتی جۆین کردن \n {es}**")


@Client.on_message(
    filters.command(
        [
            "• گۆڕینی گرووپی ئامار •",
            "• چالاککردنی گرووپی ئامار •",
            "• ناچالاککردنی گرووپی ئامار •",
        ],
        "",
    )
)
async def set_history(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        if message.command[0] == "• گۆڕینی گرووپی ئامار •":
            ask = await client.ask(
                message.chat.id, "** یوزەر یان ئایدی گرووپ بنێرە **", timeout=30
            )
            logger = ask.text
            if "@" in logger:
                logger = logger.replace("@", "")
        Botts = Bots.find({})
        for i in Botts:
            bot = client.me
            if i["bot_username"] == bot.username:
                dev = i["dev"]
                token = i["token"]
                session = i["session"]
                bot_username = i["bot_username"]
                loogger = i["logger"]
                logger_mode = i["logger_mode"]
                if message.command[0] == "• گۆڕینی گرووپی ئامار •":
                    if i["logger"] == logger:
                        return await ask.reply_text("**ئەم گرووپە هەمان گرووپە .⚡**")
                    else:
                        try:
                            user = await get_userbot(bot_username)
                            await client.send_message(logger, "**پشکنین دەکەم ...**")
                            await user.send_message(
                                logger, "**گرووپی ئامار دەگۆڕم ..**"
                            )
                            d = {"bot_username": bot_username}
                            Bots.delete_one(d)
                            asyncio.sleep(2)
                            aha = {
                                "bot_username": bot_username,
                                "token": token,
                                "session": session,
                                "dev": dev,
                                "logger": logger,
                                "logger_mode": logger_mode,
                            }
                            Bots.insert_one(aha)
                            log[bot_username] = logger
                            await ask.reply_text(
                                "**بە سەرکەوتوویی گرووپی ئامار گۆڕا ✅**"
                            )
                        except Exception:
                            await ask.reply_text(
                                "**دڵنیابە کە بۆت و ئەکاونی یاریدەدەرت زیادکردووە و کردووتە بە ئەدمین**"
                            )
                else:
                    mode = (
                        "ON"
                        if message.command[0] == "• چالاککردنی گرووپی ئامار •"
                        else "OFF"
                    )
                    if i["logger_mode"] == mode:
                        m = (
                            "چالاککراوە"
                            if message.command[0] == "• چالاککردنی گرووپی ئامار •"
                            else "ناچالاککراوە"
                        )
                        return await message.reply_text(
                            f"**گرووپی ئامار پێشتر {m} ⚡.**"
                        )
                    else:
                        try:
                            hh = {"bot_username": bot_username}
                            Bots.delete_one(hh)
                            h = {
                                "bot_username": bot_username,
                                "token": token,
                                "session": session,
                                "dev": dev,
                                "logger": loogger,
                                "logger_mode": mode,
                            }
                            Bots.insert_one(h)
                            logm[bot_username] = mode
                            m = (
                                "چالاککرا"
                                if message.command == "• چالاککردنی گرووپی ئامار •"
                                else "ناچالاککرا"
                            )
                            await message.reply_text(
                                f"**بە سەرکەوتوویی گرووپی ئامار {m}✅**"
                            )
                        except Exception as es:
                            await message.reply_text(
                                "**هەڵە ڕوویدا پەیوەندی بە گەشەپێدەر بکە ..**"
                            )
