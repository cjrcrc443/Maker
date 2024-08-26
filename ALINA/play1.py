from youtubesearchpython.__future__ import VideosSearch

import asyncio, random, os, yt_dlp, re, textwrap, aiofiles, aiohttp, numpy as np

from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)

from pyrogram import Client, filters, Client as client
from pyrogram.errors import (ChatAdminRequired,UserAlreadyParticipant,UserNotParticipant)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery 
from pyrogram.enums import ChatType, ChatMemberStatus, ParseMode

from pytgcalls.exceptions import NoActiveGroupCall, GroupCallNotFound
from pytgcalls import filters as fl
from pytgcalls.types.stream import StreamAudioEnded 
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, Update, ChatUpdate 

from config import OWNER
from Maker.ALINA import bot2, bot, pytgcalls 
from ALINA.Data import get_dev, get_dev_name
from ALINA.info import is_active, add_active, stream_on, is_streaming, stream_off, add, ddb, clear

DEV_SOURCE = "IQ7amo"


def cookies():
    cookie_dir = "ALINA/cookies"
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]

    cookie_file = os.path.join(cookie_dir, random.choice(cookies_files))
    return cookie_file
        
def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(id)s.m4a",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "quiet": True,
    "no_warnings": True,
    "prefer_ffmpeg": True,
    "cookiefile": cookies()
} 
async def download(videoid: str) -> str:
    xyz = os.path.join("downloads", f"{videoid}.m4a")
    if os.path.exists(xyz):
        return xyz
    link = f"https://youtu.be/{videoid}"
    loop = asyncio.get_event_loop()
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ytdl_data = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=True))
    file_name = ydl.prepare_filename(ytdl_data)
    return file_name



def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_thumb(videoid):
    if os.path.isfile(f"{videoid}.png"):
        return f"{videoid}.png"
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
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
                    f = await aiofiles.open(
                        f"thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(5))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype(f"plugins/utils/font.ttf", 40)
        font2 = ImageFont.truetype(f"plugins/utils/font.ttf", 70)
        arial = ImageFont.truetype(f"plugins/utils/font.ttf", 30)
        name_font = ImageFont.truetype(f"plugins/utils/font.ttf", 30)
        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text(
            (600, 150),
            "NOW PLAYING",
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
            os.remove(f"thumb{videoid}.png")
        except:
            pass
        background.save(f"{videoid}.png")
        return f"{videoid}.png"
    except:
        return f"https://telegra.ph/file/adbab8381a9d8393e10ff.jpg"
    
            

@Client.on_message(filters.command(["play", "p", "/play", "/p", "تشغيل", "شغل", "/تشغيل", "/شغل"], "") & ~filters.private & ~filters.forwarded, group=76)
async def play(client, message: Message):
    BOT_ID = client.me.id
    BOT_USERNAME = client.me.username
    user_id = message.from_user.id if message.from_user else BOT_ID
    user_name = message.from_user.first_name if message.from_user else BOT_NAME
    chat_id = message.chat.id
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("▷", callback_data=f"resume"),
        InlineKeyboardButton("II", callback_data=f"pause"),
        InlineKeyboardButton("‣‣I", callback_data="skip"),
        InlineKeyboardButton("▢", callback_data="end")],
        [InlineKeyboardButton("SoUrCe SnᎥpEr ⟁", url=f"https://t.me/SL_SN")],
        [InlineKeyboardButton(".💘اضف البوت اللي مجموعتك", url=f"https://t.me/{BOT_USERNAME}?startgroup=dream")],
    ])
    type = "audio"
    if message.reply_to_message:
        dream = await message.reply_text(f"✗┇‌◍من فضلك انتظر جارى التشغيل\n✓")
        if message.reply_to_message.audio:
            file_name = message.reply_to_message.audio
        elif message.reply_to_message.voice:
            file_name = message.reply_to_message.voice
        elif message.reply_to_message.video:
            file_name = message.reply_to_message.video
        elif message.reply_to_message.document:
            file_name = message.reply_to_message.document
        else:
            return
        if message.chat.username:
            link = "https://t.me/" + message.chat.username + '/' + str(message.reply_to_message.id)
        else:
            link = "https://t.me/c/" + str(chat_id).replace('-100','') + '/' + str(message.reply_to_message.id)
        title = file_name.file_name
        duration = seconds_to_min(file_name.duration) 
        videoid = None 
        file_path = await message.reply_to_message.download()
    else:
        if len(message.command) == 1:
            if message.chat.type == ChatType.CHANNEL:
                return await message.reply_text("✗┇‌◍قم بالرد على ملف صوتي او فيديو او اكتب تشغيل + اسم الاغنيه\n✓")
            a = await message.chat.ask("✗┇‌◍قم بإرسال اسم الاغنيه الآن\n✓", reply_to_message_id=message.id, filters=filters.user(message.from_user.id))
            query = a.text
            dream = await message.reply_text(f"✗┇‌◍جارى البحث....", reply_to_message_id=a.id)
        else:
            query = message.text.split(None, 1)[1]
            if 'https' in query and '&' in query:
                query = query.split('&')[0]
            dream = await message.reply_text(f"✗┇‌◍جارى البحث....")
        search = VideosSearch(query, limit=1)
        for data in (await search.next())["result"]: 
            try:
                title = data["title"]
                duration = data["duration"]
                videoid = data["id"]
                link = f"https://youtu.be/{videoid}"
            except Exception as e:
                return await dream.edit_text(f"✗┇‌◍حدث خطأ ما\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
        file_path = await download(videoid)
        if message.chat.type == ChatType.CHANNEL:
            if message.author_signature:
                ruser = f"[{message.author_signature}](tg://user?id={BOT_ID})"
            else:
                ruser = f"[{BOT_NAME}](tg://user?id={BOT_ID})"
        else:
            if message.from_user.first_name:
                ruser = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            else:
                ruser = f"[{message.chat.title}](tg://user?id={message.chat.id})"
    try:
        photo = await client.download_media((await client.get_users(message.from_user.id)).photo.big_file_id)
    except:
        photo = await client.download_media((await client.get_users(BOT_ID)).photo.big_file_id)
    img = await gen_thumb(videoid)
    if await is_active(chat_id):
        await add(
            chat_id,
            file_path,
            link, 
            title,
            duration,
            videoid,
            type,
            user_id,
        )
        position = len(ddb.get(chat_id)) - 1
        x = f"""
💡 **تم اضافتها الى قائمة التشغيل الدور »** `{position}`

🏷 **الاسم:** {title}
**⏱ المده:** {duration} دقيقه
🎧 **بواسطه:** {ruser}
        """
        await message.reply_photo(
            photo=img,
            caption=x,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
        await dream.delete() 
    else:
        try:
            try:
                ASS_ID = bot2.me.id
                ASS_NAME = bot2.me.first_name
                ASS_MENTION = bot2.me.mention
                ASS_USERNAME = bot2.me.username
                get = await client.get_chat_member(chat_id, ASS_ID)
            except ChatAdminRequired:
                return await dream.edit_text(f"✗┇‌◍قم باعطائي الصلاحيه التاليه:\n دعوه المستخدمين\n✓")
            if get.status == ChatMemberStatus.BANNED:
                try:
                    await client.unban_chat_member(chat_id, ASS_ID)
                except:
                    unban_butt = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text=f"• الغاء حظر المساعد •",
                                    callback_data=f"unban_assistant {chat_id}|{ASS_ID}",
                                ),
                            ]
                        ]
                    )
                    return await dream.edit_text(f"✗┇‌◍الحساب المساعد تم حظره في الجروب\n✗┇‌◍اسم المساعد {ASS_MENTION}\n✗┇‌◍ايدي المساعد `{ASS_ID}`\n✗┇‌◍يوزر المساعد @{ASS_USERNAME}\n✓", reply_markup=unban_butt)
        except UserNotParticipant:
            chat = await client.get_chat(chat_id)
            if chat.username:
                try:
                    await bot2.join_chat(chat.username)
                except UserAlreadyParticipant:
                    try:
                        invitelink = (await client.export_chat_invite_link(chat_id))
                        if invitelink.startswith("https://t.me/+"):
                            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                        await asyncio.sleep(2)
                        await bot2.join_chat(invitelink)
                    except ChatAdminRequired:
                        return await dream.edit_text(f"✗┇‌◍قم باعطائي الصلاحيه التاليه:\n دعوه المستخدمين\n✓")
                    except Exception as e:
                        return await dream.edit(f"✗┇‌◍الحساب المساعد فشل فى الدخول الى الجروب بسبب:\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
            else:
                try:
                    try:
                        invitelink = chat.invite_link
                        if invitelink is None:
                            invitelink = (await client.export_chat_invite_link(chat_id))
                    except Exception:
                        try:
                            invitelink = (await client.export_chat_invite_link(chat_id))
                        except ChatAdminRequired:
                            return await dream.edit_text(f"✗┇‌◍قم باعطائي الصلاحيه التاليه:\n دعوه المستخدمين\n✓")
                        except Exception as e:
                            await dream.edit(f"✗┇‌◍الحساب المساعد فشل فى الدخول الى الجروب بسبب:\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await bot2.join_chat(invitelink)
                except Exception as e:
                    await dream.edit_text(f"✗┇‌◍الحساب المساعد فشل فى الدخول الى الجروب بسبب:\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
        try:
            
            await pytgcalls.play(chat_id, MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM))  
        except (NoActiveGroupCall, GroupCallNotFound):
            return await dream.edit_text("✗┇‌◍قم بفتح الكول اولا فى الجروب\n✓")  
        except Exception as e:
            if 'CreateGroupCall' in str(e):
                return await dream.edit_text("✗┇‌◍قم بفتح الكول اولا فى الجروب\n✓")  
            else:
                return await dream.edit_text(f"{e}\n✗┇‌◍في حاله ظهور لك مثل هذه المشكله تواصل مع المطور -> @{DEV_SOURCE}")
        ruser = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        await stream_on(chat_id)
        await add_active(chat_id)
        await add(
            chat_id,
            file_path,
            link, 
            title,
            duration,
            videoid,
            type,
            user_id,
        )
        x = f"""
💡 **تم تشغيل الموسيقى.**

🏷 **الاسم:** {title}
**⏱ المده:** {duration} دقيقه
🎧 **بواسطه:** {ruser}
        """
        await message.reply_photo(
            photo=img,
            caption=x,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN, 
        )
        await dream.delete()

@Client.on_message(filters.command(["vplay", "vp", "/vplay", "/vp", "فيديو", "فيد", "/فيديو", "/فيد"], "") & ~filters.private & ~filters.forwarded, group=776)
async def vplay(client, message: Message):
    BOT_ID = client.me.id
    BOT_USERNAME = client.me.username
    user_id = message.from_user.id if message.from_user else BOT_ID
    user_name = message.from_user.first_name if message.from_user else BOT_NAME
    chat_id = message.chat.id
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("▷", callback_data=f"resume"),
        InlineKeyboardButton("II", callback_data=f"pause"),
        InlineKeyboardButton("‣‣I", callback_data="skip"),
        InlineKeyboardButton("▢", callback_data="end")],
        [InlineKeyboardButton("SoUrCe SnᎥpEr ⟁", url=f"https://t.me/SL_SN")],
        [InlineKeyboardButton(".💘اضف البوت اللي مجموعتك", url=f"https://t.me/{BOT_USERNAME}?startgroup=dream")],
    ])
    type = "video"
    if message.reply_to_message:
        dream = await message.reply_text(f"✗┇‌◍من فضلك انتظر جارى التشغيل\n✓")
        if message.reply_to_message.audio:
            file_name = message.reply_to_message.audio
        elif message.reply_to_message.voice:
            file_name = message.reply_to_message.voice
        elif message.reply_to_message.video:
            file_name = message.reply_to_message.video
        elif message.reply_to_message.document:
            file_name = message.reply_to_message.document
        else:
            return
        if message.chat.username:
            link = "https://t.me/" + message.chat.username + '/' + str(message.reply_to_message.id)
        else:
            link = "https://t.me/c/" + str(chat_id).replace('-100','') + '/' + str(message.reply_to_message.id)
        title = file_name.file_name
        duration = seconds_to_min(file_name.duration) 
        videoid = None 
        file_path = None
        link = await message.reply_to_message.download()
    else:
        if len(message.command) == 1:
            if message.chat.type == ChatType.CHANNEL:
                return await message.reply_text("✗┇‌◍قم بالرد على ملف صوتي او فيديو او اكتب تشغيل + اسم الاغنيه\n✓")
            a = await message.chat.ask("✗┇‌◍قم بإرسال اسم الاغنيه الآن\n✓", reply_to_message_id=message.id, filters=filters.user(message.from_user.id))
            query = a.text
            dream = await message.reply_text(f"✗┇‌◍جارى البحث....", reply_to_message_id=a.id)
        else:
            query = message.text.split(None, 1)[1]
            if 'https' in query and '&' in query:
                query = query.split('&')[0]
            dream = await message.reply_text(f"✗┇‌◍جارى البحث....")
        search = VideosSearch(query, limit=1)
        for data in (await search.next())["result"]: 
            try:
                title = data["title"]
                videoid = data["id"]
                duration = data["duration"]
                link = f"https://youtu.be/{videoid}"
            except Exception as e:
                return await dream.edit_text(f"✗┇‌◍حدث خطأ ما\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
        file_path = None
        if message.chat.type == ChatType.CHANNEL:
            if message.author_signature:
                ruser = f"[{message.author_signature}](tg://user?id={BOT_ID})"
            else:
                ruser = f"[{BOT_NAME}](tg://user?id={BOT_ID})"
        else:
            if message.from_user.first_name:
                ruser = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            else:
                ruser = f"[{message.chat.title}](tg://user?id={message.chat.id})"
    try:
        photo = await client.download_media((await client.get_users(message.from_user.id)).photo.big_file_id)
    except:
        photo = await client.download_media((await client.get_users(BOT_ID)).photo.big_file_id)
    img = await gen_thumb(videoid)
    if await is_active(chat_id):
        await add(
            chat_id,
            file_path,
            link, 
            title,
            duration,
            videoid,
            type,
            user_id,
        )
        position = len(ddb.get(chat_id)) - 1
        x = f"""
💡 **تم اضافتها الى قائمة التشغيل الدور »** `{position}`

🏷 **الاسم:** {title}
**⏱ المده:** {duration} دقيقه
🎧 **بواسطه:** {ruser}
        """
        await message.reply_photo(
            photo=img,
            caption=x,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
        await dream.delete() 
    else:
        try:
            try:
                ASS_ID = bot2.me.id
                ASS_NAME = bot2.me.first_name
                ASS_MENTION = bot2.me.mention
                ASS_USERNAME = bot2.me.username
                get = await client.get_chat_member(chat_id, ASS_ID)
            except ChatAdminRequired:
                return await dream.edit_text(f"✗┇‌◍قم باعطائي الصلاحيه التاليه:\n دعوه المستخدمين\n✓")
            if get.status == ChatMemberStatus.BANNED:
                try:
                    await client.unban_chat_member(chat_id, ASS_ID)
                except:
                    unban_butt = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text=f"• الغاء حظر المساعد •",
                                    callback_data=f"unban_assistant {chat_id}|{ASS_ID}",
                                ),
                            ]
                        ]
                    )
                    return await dream.edit_text(f"✗┇‌◍الحساب المساعد تم حظره في الجروب\n✗┇‌◍اسم المساعد {ASS_MENTION}\n✗┇‌◍ايدي المساعد `{ASS_ID}`\n✗┇‌◍يوزر المساعد @{ASS_USERNAME}\n✓", reply_markup=unban_butt)
        except UserNotParticipant:
            chat = await client.get_chat(chat_id)
            if chat.username:
                try:
                    await bot2.join_chat(chat.username)
                except UserAlreadyParticipant:
                    try:
                        invitelink = (await client.export_chat_invite_link(chat_id))
                        if invitelink.startswith("https://t.me/+"):
                            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                        await asyncio.sleep(2)
                        await bot2.join_chat(invitelink)
                    except ChatAdminRequired:
                        return await dream.edit_text(f"✗┇‌◍قم باعطائي الصلاحيه التاليه:\n دعوه المستخدمين\n✓")
                    except Exception as e:
                        return await dream.edit(f"✗┇‌◍الحساب المساعد فشل فى الدخول الى الجروب بسبب:\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
            else:
                try:
                    try:
                        invitelink = chat.invite_link
                        if invitelink is None:
                            invitelink = (await client.export_chat_invite_link(chat_id))
                    except Exception:
                        try:
                            invitelink = (await client.export_chat_invite_link(chat_id))
                        except ChatAdminRequired:
                            return await dream.edit_text(f"✗┇‌◍قم باعطائي الصلاحيه التاليه:\n دعوه المستخدمين\n✓")
                        except Exception as e:
                            await dream.edit(f"✗┇‌◍الحساب المساعد فشل فى الدخول الى الجروب بسبب:\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await bot2.join_chat(invitelink)
                except Exception as e:
                    await dream.edit_text(f"✗┇‌◍الحساب المساعد فشل فى الدخول الى الجروب بسبب:\n`{e}`\nفى حاله ظهور لك مثلا هذه الرساله تواصل مع المطور -> @{DEV_SOURCE}")
        try:
            await pytgcalls.play(chat_id, MediaStream(link, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.SD_480p))  
        except (NoActiveGroupCall, GroupCallNotFound):
            return await dream.edit_text("✗┇‌◍قم بفتح الكول اولا فى الجروب\n✓")  
        except Exception as e:
            if 'CreateGroupCall' in str(e):
                return await dream.edit_text("✗┇‌◍قم بفتح الكول اولا فى الجروب\n✓")  
            else:
                return await dream.edit_text(f"{e}\n✗┇‌◍في حاله ظهور لك مثل هذه المشكله تواصل مع المطور -> @iq7amo")
        await stream_on(chat_id)
        await add_active(chat_id)
        await add(
            chat_id,
            file_path,
            link, 
            title,
            duration,
            videoid,
            type,
            user_id,
        )
        x = f"""
💡 **بدء تشغيل الفيديو.**

🏷 **الاسم:** {title}
**⏱ المده:** {duration} دقيقه
🎧 **بواسطه:** {ruser}
        """
        await message.reply_photo(
            photo=img,
            caption=x,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN, 
        )
        await dream.delete()


@Client.on_callback_query(filters.regex(pattern=r"^(resume|pause|skip|end)$"))
async def admin_cbs(c: Client, query: CallbackQuery):
    a = await c.get_chat_member(query.message.chat.id, query.from_user.id)
    bot_username = c.me.username
    dev = await get_dev(bot_username)
    if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
     if not query.from_user.id == dev:
      if not query.from_user.username in OWNER:
        return await query.answer("پێویستە ئەدمین بیت بۆ کردنی ئەم کارە !", show_alert=True)
        if not await is_active(query.message.chat.id):
            return await query.answer("✗┇‌◍مفيش حاجه شغاله 🙄❤\n✓️", show_alert=True)
        chat_id = query.message.chat.id
        data = query.matches[0].group(1)

        if data == "resume":
            if await is_streaming(chat_id):
                return await query.answer(
                    "الموسيقى مستأنفه بالفعل.", show_alert=True
                )
            await stream_on(chat_id)
            await pytgcalls.resume_stream(query.message.chat.id)
            await query.message.reply_text(
                text=f"✗┇‌◍تم اسئناف الموسيقى بواسطه »\n!❲[{query.from_user.first_name}](tg://user?id={query.from_user.id})❳!",
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "pause":
            if not await is_streaming(chat_id):
                return await query.answer(
                    "الموسيقى متوقفه مؤقتا بالفعل.", show_alert=True
                )
            await stream_off(chat_id)
            await pytgcalls.pause_stream(query.message.chat.id)
            await query.message.reply_text(
                text=f"✗┇‌◍تم ايقاف التشغيل مؤقتا بواسطه »\n!❲[{query.from_user.first_name}](tg://user?id={query.from_user.id})❳!",
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "end":
            try:
                await clear(query.message.chat.id)
                await pytgcalls.leave_call(query.message.chat.id)
            except:
                pass
            await query.message.reply_text(
                text=f"✗┇‌◍تم ايقاف التشغيل بواسطه »\n!❲[{query.from_user.first_name}](tg://user?id={query.from_user.id})❳!",
                parse_mode=ParseMode.MARKDOWN,
            )

        elif data == "skip":
            get = ddb.get(chat_id)
            popped = get.pop(0)
            if not get:
                await pytgcalls.leave_call(chat_id)
                await clear(chat_id)
                return await query.message.reply_text(f"✗┇‌◍لا يوجد شيء في قائمة الانتظار خروج المساعد من المحادثه الصوتيه بواسطه »\n!❲[{query.from_user.first_name}](tg://user?id={query.from_user.id})❳!", parse_mode=ParseMode.MARKDOWN)
            else:
                link = get[0]["link"]
                title = get[0]["title"]
                duration = get[0]["duration"]
                videoid = get[0]["videoid"]
                file_path = get[0]["file_path"]
                user_id = get[0]["user_id"]
                type = get[0]["type"]
                userx = await c.get_users(user_id)
                req_by = userx.mention
                if type == "audio":
                    stream = MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM)
                else:
                    stream = MediaStream(link, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.SD_480p)
                try:
                    await pytgcalls.play(
                        query.message.chat.id,
                        stream,
                    )
                except Exception as ex:
                    print(ex)
                    await clear(query.message.chat.id)
                    return await pytgcalls.leave_call(query.message.chat.id)
                try:
                    photo = await c.download_media((await c.get_users(query.from_user.id)).photo.big_file_id)
                except:
                    photo = await c.download_media((await c.get_users(BOT_ID)).photo.big_file_id)
                img = await gen_thumb(videoid)
                await query.edit_message_text(
                    text=f"✗┇‌◍Skipped by »\n!❲[{query.from_user.first_name}](tg://user?id={query.from_user.id})❳!",
                    parse_mode=ParseMode.MARKDOWN,
                )
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton("▷", callback_data=f"resume"),
                    InlineKeyboardButton("II", callback_data=f"pause"),
                    InlineKeyboardButton("‣‣I", callback_data="skip"),
                    InlineKeyboardButton("▢", callback_data="end")],
                    [InlineKeyboardButton("SoUrCe SnᎥpEr ⟁", url=f"https://t.me/SL_SN")],
                    [InlineKeyboardButton(".💘اضف البوت اللي مجموعتك", url=f"https://t.me/{c.me.username}?startgroup=dream")],
                ])
                return await query.message.reply_photo(
                    photo=img,
                    caption=f"⏭ **تم التخطي للمسار التالي.**\n\n🏷 **الاسم:** {title}\n**⏱ المده:** {duration} دقيقه\n🎧 **طلب بواسطه:** {req_by}",
                    reply_markup=keyboard,
                    parse_mode=ParseMode.MARKDOWN,
                )
    else:
        return await query.answer("يجب ان تكون ادمن لاستخدام هذا الامر", show_alert=True)

@Client.on_message(filters.command(["stop", "end", "/stop", "/end", "ايقاف", "وقف", "انهاء", "/ايقاف", "/وقف", "/انهاء", "تخطي", "/تخطي", "skip", "/skip", "/pause", "/resume", "/next", "next"], "") & filters.group, group=988)
@Client.on_edited_message(filters.command(["stop", "end", "/stop", "/end", "ايقاف", "وقف", "انهاء", "/ايقاف", "/وقف", "/انهاء", "تخطي", "/تخطي", "skip", "/skip", "/pause", "/resume", "/next", "next"], "") & filters.group,group=988)
async def cmd_admins(c, msg):
    a = await c.get_chat_member(msg.chat.id, msg.from_user.id)
    bot_username = c.me.username
    dev = await get_dev(bot_username)
    if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
     if not msg.from_user.id == dev:
      if not msg.from_user.username in OWNER:
        return await msg.answer("پێویستە ئەدمین بیت بۆ کردنی ئەم کارە !", show_alert=True)
        if not await is_active(msg.chat.id):
            return await msg.reply("✗┇‌◍مفيش حاجه شغاله 🙄❤\n✓️")
        chat_id = msg.chat.id
        command = msg.command[0]
        bot_user = c.me.username
        if command == "/pause":
            if not await is_streaming(chat_id):
                return await msg.reply_text("✗┇‌◍الموسيقى متوقفه مؤقتا بالفعل\n✓️")
            await pytgcalls.pause_stream(chat_id)
            await stream_off(chat_id)
            return await msg.reply_text(f"✗┇‌◍تم ايقاف التشغيل مؤقتا بواسطه »\n!❲[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})❳!", parse_mode=ParseMode.MARKDOWN)
        elif command == "/resume":
            if await is_streaming(chat_id):
                return await msg.reply_text("✗┇‌◍الموسيقى مستئنفه بالفعل\n✓️")
            await pytgcalls.resume_stream(chat_id)
            await stream_on(chat_id)
            return await msg.reply_text(f"✗┇‌◍تم استئناف التشغيل بواسطه »\n!❲[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})❳!", parse_mode=ParseMode.MARKDOWN)
        elif command == "/stop" or command == "/end" or command == "stop" or command == "end" or command == "ايقاف" or command == "انهاء" or command == "وقف" or command == "/ايقاف" or command == "/انهاء" or command == "/وقف":
            try:
                await pytgcalls.leave_call(chat_id)
            except:
                pass
            await clear(chat_id)
            return await msg.reply_text(f"✗┇‌◍تم ايقاف التشغيل بواسطه »\n!❲[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})❳!", parse_mode=ParseMode.MARKDOWN)
        elif command == "/skip" or command == "/next" or command == "/تخطي" or command == "skip" or command == "next" or command == "تخطي":
            check = ddb.get(chat_id)
            popped = check.pop(0)
            if not check:
                await pytgcalls.leave_call(chat_id)
                await clear(chat_id)
                return await msg.reply_text(f"✗┇‌◍لا يوجد شيء في قائمة الانتظار خروج المساعد من المحادثه الصوتيه بواسطه »\n!❲[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})❳!", parse_mode=ParseMode.MARKDOWN)
            link = get[0]["link"]
            title = get[0]["title"]
            duration = get[0]["duration"]
            videoid = get[0]["videoid"]
            file_path = get[0]["file_path"]
            user_id = get[0]["user_id"]
            type = get[0]["type"]
            try:
                file_path = file
            except:     
                try:
                    file_path = await download(videoid)
                except:
                    print(f"Admins: {e}") 
            if type == "video":
                stream = MediaStream(link, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.SD_480p)
            else:
                stream = MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM)
            try:
                await pytgcalls.play(chat_id, stream)
            except Exception:
                await clear(chat_id)
                return await pytgcalls.leave_call(chat_id)
            userx = await c.get_users(user_id)
            img = await gen_thumb(videoid)
            requester = userx.mention       
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("▷", callback_data=f"resume"),
                InlineKeyboardButton("II", callback_data=f"pause"),
                InlineKeyboardButton("‣‣I", callback_data=f"skip"),
                InlineKeyboardButton("▢", callback_data=f"end")],
                [InlineKeyboardButton("SoUrCe SnᎥpEr ⟁", url="https://t.me/SL_SN")],
                [InlineKeyboardButton(".💘اضف البوت اللي مجموعتك", url=f"https://t.me/{bot_user}?startgroup=dream")],
            ])
            await msg.reply_photo(photo=img, caption=f"⏭ **تم التخطي للمسار التالي.**\n\n🏷 **الاسم:** {title}\n**⏱ المده:** {dur} دقيقه\n🎧 **طلب بواسطه:** {requester}", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            try:
                os.remove(img)
            except:
                pass
    else:
        return await msg.reply("يجب ان تكون ادمن لاستخدام هذا الامر")

@Client.on_message(filters.video_chat_started, group=20)
@Client.on_message(filters.video_chat_ended, group=30)
async def welcomee(c, msg):
    try:
        await clear(msg.chat.id)
        await pytgcalls.leave_call(msg.chat.id)
    except:
        pass

@Client.on_message(filters.left_chat_member, group=65)
async def ub_leave(c, msg):
    if msg.left_chat_member.id == c.me.id:
        try:
            await clear(msg.chat.id)
            await pytgcalls.leave_call(msg.chat.id)
        except:
            pass
        try:
            await bot2.leave_chat(msg.chat.id)
        except:
            pass

@pytgcalls.on_update(fl.chat_update(ChatUpdate.Status.KICKED | ChatUpdate.Status.LEFT_GROUP))
async def swr_handler(_, chat_id: int):
    try:
        await clear(chat_id)
    except:
        pass


async def change_stream(client, chat_id):
    try:
        get = ddb.get(chat_id)
        try:
            popped = get.pop(0)
        except:
            pass
        if not get:
            await clear(chat_id)
            return await client.leave_call(chat_id)
        link = get[0]["link"]
        title = get[0]["title"]
        duration = get[0]["duration"]
        videoid = get[0]["videoid"]
        file_path = get[0]["file_path"]
        user_id = get[0]["user_id"]
        type = get[0]["type"]
        get[0]["played"] = 0
        if not videoid:
            file_path = file_path
        else:
            try:
                file_path = await download(videoid)
            except Exception as e:
                print(f"chang_stream {e}")
            if type == "video":
                stream = MediaStream(link, audio_parameters=AudioQuality.MEDIUM, video_parameters=VideoQuality.SD_480p)
            else:
                stream = MediaStream(file_path, audio_parameters=AudioQuality.MEDIUM)
            try:
                await client.play(chat_id, stream)
            except Exception as e:
                await bot.send_message(chat_id, str(e))
            userx = await bot.get_users(user_id)
            img = await gen_thumb(videoid)
            requester = userx.mention
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("▷", callback_data=f"resume"),
                InlineKeyboardButton("II", callback_data=f"pause"),
                InlineKeyboardButton("‣‣I", callback_data="skip"),
                InlineKeyboardButton("▢", callback_data="end")],
                [InlineKeyboardButton("SoUrCe SnᎥpEr ⟁", url=f"https://t.me/SL_SN")],
                [InlineKeyboardButton(".💘اضف البوت اللي مجموعتك", url=f"https://t.me/{bot.me.username}?startgroup=dream")],
            ])
            await app.send_photo(chat_id, photo=img, caption=f"⏭ **تم التخطي للمسار التالي.**\n\n🏷 **الاسم:** {title}\n**⏱ المده:** {duration} دقيقه\n🎧 **بواسطه:** {requester}", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            try:
                os.remove(img)
            except:
                pass
    except Exception as e:
        await app.send_message(chat_id, str(e))

@pytgcalls.on_update(fl.stream_end)
async def stream_end_handler1(client, update: Update):
    if not isinstance(update, StreamAudioEnded):
        return
    await change_stream(client, update.chat_id)

@Client.on_message(filters.regex("^المساعد$|^الحساب المساعد$|^• المساعد •$|^• الحساب المساعد •$"), group=896)
async def assistant(c: Client, m: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"{bot2.me.first_name}", user_id=bot2.me.id)],
        [InlineKeyboardButton(".💘اضف البوت اللي مجموعتك", url=f"https://t.me/{c.me.username}?startgroup=dream")],
    ])
    if bot2.me.photo:
        photo = await bot2.download_media(user.me.photo.big_file_id)
        await m.reply_photo(photo, caption=f"✗┇‌◍الحساب المساعد الخاص بالبوت:\n{bot2.me.mention}\n✓", reply_markup=keyboard)
        try:
            os.remove(photo)
        except:
            pass
    else:
        await m.reply_text(f"✗┇‌◍الحساب المساعد الخاص بالبوت:\n{user.me.mention}\n✓", reply_markup=keyboard)
        
