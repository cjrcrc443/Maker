import asyncio
import os
import re
import textwrap
from typing import Union

import aiofiles
import aiohttp
import yt_dlp
from googletrans import Translator
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded, StreamVideoEnded
from youtubesearchpython.__future__ import VideosSearch

from ALINA.Data import (
    get_call,
    get_channel,
    get_data,
    get_group,
    get_userbot,
    must_join,
)
from config import MONGO_DB_URL, OWNER, VIDEO, appp

translator = Translator()


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


ahmed = "https://graph.org/file/c8d0d49f5e13290314807.jpg"


async def gen_thumb(videoid, photo):
    if os.path.isfile(f"{photo}.png"):
        return f"{photo}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
                test = translator.translate(title, dest="en")
                title = test.text
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"thumb{videoid}.png")
        ALINAv = Image.open(f"{photo}")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(5))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = ALINAv.width / 2
        Ycenter = ALINAv.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = ALINAv.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("font2.ttf", 40)
        font2 = ImageFont.truetype("font2.ttf", 70)
        arial = ImageFont.truetype("font2.ttf", 30)
        name_font = ImageFont.truetype("font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text(
            (600, 150),
            "HAWAL PLAYING",
            fill="white",
            stroke_width=2,
            stroke_fill="white",
            font=font2,
        )
        for line in para:
            if j == 1:
                j += 1
                draw.text(
                    (600, 340),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
            if j == 0:
                j += 1
                draw.text(
                    (600, 280),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )

        draw.text(
            (600, 450),
            f"Views : {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 500),
            f"Duration : {duration[:23]} Mins",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 550),
            f"Channel : {channel}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"{photo}")
            os.remove(f"thumb{videoid}.png")
        except:
            pass
        background.save(f"{photo}.png")
        return f"{photo}.png"
    except Exception:
        return ahmed


mongodb = _mongo_client_(MONGO_DB_URL)


db = {}


async def add(
    chat_id, bot_username, file_path, link, title, duration, videoid, vid, user_id
):
    put = {
        "title": title,
        "dur": duration,
        "user_id": user_id,
        "chat_id": chat_id,
        "vid": vid,
        "file_path": file_path,
        "link": link,
        "videoid": videoid,
        "played": 0,
    }
    chat_id = f"{bot_username}{chat_id}"
    i = db.get(chat_id)
    if not i:
        db[chat_id] = []
    db[chat_id].append(put)
    return


# Users


async def is_served_user(client, user_id: int) -> bool:
    userdb = await get_data(client)
    userdb = userdb.users
    user = await userdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users(client) -> list:
    userdb = await get_data(client)
    userdb = userdb.users
    users_list = []
    async for user in userdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(client, user_id: int):
    userdb = await get_data(client)
    userdb = userdb.users
    is_served = await is_served_user(client, user_id)
    if is_served:
        return
    return await userdb.insert_one({"user_id": user_id})


async def del_served_user(client, user_id: int):
    chats = await get_data(client)
    chatsdb = chats.users
    is_served = await is_served_user(client, user_id)
    if not is_served:
        return
    return await chatsdb.delete_one({"user_id": user_id})


# Served Chats


async def get_served_chats(client) -> list:
    chats = await get_data(client)
    chatsdb = chats.chats
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(client, chat_id: int) -> bool:
    chats = await get_data(client)
    chatsdb = chats.chats
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(client, chat_id: int):
    chats = await get_data(client)
    chatsdb = chats.chats
    is_served = await is_served_chat(client, chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


async def del_served_chat(client, chat_id: int):
    chats = await get_data(client)
    chatsdb = chats.chats
    is_served = await is_served_chat(client, chat_id)
    if not is_served:
        return
    return await chatsdb.delete_one({"chat_id": chat_id})


# Served Call

activecall = {}


async def get_served_call(bot_username) -> list:
    return activecall[bot_username]


async def is_served_call(client, chat_id: int) -> bool:
    bot_username = client.me.username
    if chat_id not in activecall[bot_username]:
        return False
    else:
        return True


async def add_served_call(client, chat_id: int):
    bot_username = client.me.username
    if chat_id not in activecall[bot_username]:
        activecall[bot_username].append(chat_id)


async def remove_served_call(bot_username, chat_id: int):
    if chat_id in activecall[bot_username]:
        activecall[bot_username].remove(chat_id)


# Active Voice Chats
active = []


async def get_active_chats() -> list:
    return active


async def is_active_chat(chat_id: int) -> bool:
    if chat_id not in active:
        return False
    else:
        return True


async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)


async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)


# Active Video Chats
activevideo = []


async def get_active_video_chats() -> list:
    return activevideo


async def is_active_video_chat(chat_id: int) -> bool:
    if chat_id not in activevideo:
        return False
    else:
        return True


async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)


async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)


async def remove_active(bot_username, chat_id: int):
    chat = f"{bot_username}{chat_id}"
    try:
        db[chat] = []
    except:
        pass
    try:
        await remove_active_video_chat(chat_id)
    except:
        pass
    try:
        await remove_active_chat(chat_id)
    except:
        pass
    try:
        await remove_served_call(bot_username, chat_id)
    except:
        pass


async def download(bot_username, link, video: Union[bool, str] = None):
    link = link
    loop = asyncio.get_running_loop()

    def audio_dl():
        ydl_optssx = {
            "format": "bestaudio/best",
            "outtmpl": f"downloads/{bot_username}%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
        }
        x = yt_dlp.YoutubeDL(ydl_optssx)
        info = x.extract_info(link, False)
        xyz = os.path.join("downloads", f"{bot_username}{info['id']}.{info['ext']}")
        if os.path.exists(xyz):
            return xyz
        x.download([link])
        return xyz

    if video:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            downloaded_file = stdout.decode().split("\n")[0]
        else:
            return
    else:
        downloaded_file = await loop.run_in_executor(None, audio_dl)
    return downloaded_file


async def change_stream(bot_username, client, chat_id):
    try:
        chat = f"{bot_username}{chat_id}"
        check = db.get(chat)
        try:
            popped = check.pop(0)
        except:
            pass
        if not check:
            await remove_active(bot_username, chat_id)
            try:
                return await client.leave_group_call(chat_id)
            except:
                return
        file_path = check[0]["file_path"]
        title = check[0]["title"]
        dur = check[0]["dur"]
        user_id = check[0]["user_id"]
        chat_id = check[0]["chat_id"]
        video = check[0]["vid"]
        audio_stream_quality = HighQualityAudio()
        video_stream_quality = MediumQualityVideo()
        videoid = check[0]["videoid"]
        link = check[0]["videoid"]
        check[0]["played"] = 0
        app = appp[bot_username]
        if not link:
            file_path = file_path
        else:
            try:
                file_path = await download(bot_username, link, video)
            except Exception as es:
                return await app.send_message(
                    chat_id, f"**⎆┊ هەڵە ڕوویدا لە کاتی پەخشی دواتر 🎸•**"
                )
        stream = (
            AudioVideoPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(file_path, audio_parameters=audio_stream_quality)
        )
        try:
            await client.change_stream(chat_id, stream)
        except Exception as es:
            return await app.send_message(
                chat_id, f"**⎆┊ هەڵە ڕوویدا لە کاتی پەخشی دواتر 🎸•**"
            )
        userx = await app.get_users(user_id)
        if videoid:
            ahmed = await app.get_chat(OWNER[0])
            photo_id = ahmed.photo.big_file_id
            photo = await app.download_media(photo_id)
            img = await gen_thumb(videoid, photo)
        else:
            img = VIDEO
        requester = userx.mention
        bot_username = client.me.username
        dev = await get_dev(bot.username)
        devname = await get_dev_name(client, bot.username)
        gr = await get_group(bot_username)
        ch = await get_channel(bot_username)
        button = [
            [
                InlineKeyboardButton(text="𝗘𝗻𝗱 🎸•", callback_data=f"stop"),
                InlineKeyboardButton(text="𝗥𝗲𝘀𝘂𝗺𝗲 🎸•", callback_data=f"resume"),
                InlineKeyboardButton(text="𝗣𝗮𝘂𝘀𝗲 🎸•", callback_data=f"pause"),
            ],
            [
                InlineKeyboardButton(text="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🖱️", url=f"{ch}"),
                InlineKeyboardButton(text="𝗚𝗿𝗼𝘂𝗽 🖱️", url=f"{gr}"),
            ],
            [InlineKeyboardButton(f"{devname} 💸•", user_id=f"{dev}")],
            [
                InlineKeyboardButton(
                    text="⌯ زیادم بکە بۆ گرووپ یان کەناڵت ⚡️•",
                    url=f"https://t.me/{bot_username}?startgroup=True",
                )
            ],
        ]
        await app.send_photo(
            chat_id,
            photo=img,
            caption=f"**⭓ᴍᴜˢɪᴄ✘ʜᴀᴡᴀʟ 🎻\n\n╮◉ ناونیشان : {title}\n│᚜⦿ ماوەکەی : {duration} ⌚\n╯◉ لەلایەن : {requester}**",
            reply_markup=InlineKeyboardMarkup(button),
        )
        try:
            os.remove(file_path)
            os.remove(img)
        except:
            pass
    except:
        pass


async def helper(bot_username):
    user = await get_userbot(bot_username)
    gr = await get_group(bot_username)


async def Call(bot_username):
    call = await get_call(bot_username)

    @call.on_kicked()
    @call.on_closed_voice_chat()
    @call.on_left()
    async def stream_services_handler(client, chat_id: int):
        return await remove_active(bot_username, chat_id)

    @call.on_stream_end()
    async def stream_end_handler1(client: PyTgCalls, update: Update):
        if not isinstance(update, (StreamVideoEnded, StreamAudioEnded)):
            return
        await change_stream(bot_username, client, update.chat_id)


async def joinch(message):
    ii = await must_join(message._client.me.username)
    if ii == "off":
        return
    cch = await get_channel(message._client.me.username)
    ch = cch.replace("https://t.me/", "")
    try:
        await message._client.get_chat_member(ch, message.from_user.id)
    except UserNotParticipant:
        try:
            await message.reply(
                f"**◗⋮◖ پێویستە جۆینی کەناڵ بکەیت\n\n◗⋮◖ کەناڵی بۆت : « {cch} »**",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("جۆینی کەناڵ بکە ◗⋮◖", url=f"{cch}"),
                        ],
                    ]
                ),
            )
            return True
        except Exception as a:
            print(a)
    except Exception as a:
        print(a)
