from pyrogram import Client, filters
from youtubesearchpython.__future__ import VideosSearch 
import os
import aiohttp
import requests
import random 
import asyncio
import yt_dlp
from datetime import datetime, timedelta
from youtube_search import YoutubeSearch
import pytgcalls
from pytgcalls.types import (
    MediaStream,
    AudioQuality,
    VideoQuality,
    Update,
)
from typing import Union
from pyrogram import Client, filters 
from pyrogram import Client as client
from pyrogram.errors import (ChatAdminRequired,
                             UserAlreadyParticipant,
                             UserNotParticipant)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls import PyTgCalls
from ntgcalls import TelegramServerError
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types.stream import StreamAudioEnded
from config import API_ID, API_HASH, MONGO_DB_URL, VIDEO, OWNER, OWNER_NAME, LOGS, GROUP, CHANNEL
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from bot import bot as man
from ALINA.info import (db, add, is_served_call, add_active_video_chat, add_served_call, add_active_chat, gen_thumb, download, remove_active, joinch)
from ALINA.Data import (get_logger, get_userbot, get_call, get_logger_mode, get_group, get_channel, get_dev_name, get_dev)
import asyncio
             
mongodb = _mongo_client_(MONGO_DB_URL)
pymongodb = MongoClient(MONGO_DB_URL)
Bots = pymongodb.Bots


async def join_assistant(client, chat_id, message_id, userbot, file_path):
        join = None
        try:
            try:
                user = userbot.me
                user_id = user.id
                get = await client.get_chat_member(chat_id, user_id)
            except ChatAdminRequired:
                await client.send_message(chat_id, f"**⎆┊ بۆت بکە ئەدمین ئەزیزم 🧑🏻‍💻•**", reply_to_message_id=message_id)
            if get.status == ChatMemberStatus.BANNED:
                await client.send_message(chat_id, f"**⎆┊ بۆ چالاککردنی بۆتەکە ئەکاونتی یاریدەدەرەکە باندی لابە •\n\n⎆┊ ئەکاونتی یاریدەدەرە : @{user.username} •\n⎆┊ دڵنیا بە کا لادراوە لە باند •\n\n⎆┊ یان پەیوەندی بە گەشەپێدەرەوە بکە لە لێرە : {GROUP}•**", reply_to_message_id=message_id)
            else:
              join = True
        except UserNotParticipant:
            chat = await client.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                    join = True
                except UserAlreadyParticipant:
                    join = True
                except Exception:
                 try:
                  invitelink = (await client.export_chat_invite_link(chat_id))
                  if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                  await asyncio.sleep(3)
                  await userbot.join_chat(invitelink)
                  join = True
                 except ChatAdminRequired:
                    return await client.send_message(chat_id, f"**⎆┊ ڕۆڵ بدە بە بۆتەکە بۆ زیادکردنی بەکارهێنەر لە ڕێگەی لینکەوە •**", reply_to_message_id=message_id)
                 except Exception as e:
                   await client.send_message(chat_id, f"**⎆┊ هەڵەیەک ڕوویدا، دواتر هەوڵبدەرەوە•\n⎆┊ {GROUP} : یان لێرەوە پەیوەندی بکە •**", reply_to_message_id=message_id)
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
                          await client.send_message(chat_id, f"**⎆┊ ڕۆڵ بدە بە بۆتەکە بۆ زیادکردنی بەکارهێنەر لە ڕێگەی لینکەوە •**", reply_to_message_id=message_id)
                        except Exception as e:
                          await client.send_message(chat_id, f"**⎆┊ هەڵەیەک ڕوویدا، دواتر هەوڵبدەرەوە•\n⎆┊ {GROUP} : یان لێرەوە پەیوەندی بکە •**", reply_to_message_id=message_id)
                    m = await client.send_message(chat_id, "**⎆┊ کەمێك چاوەڕێ بکە تا بۆتەکە چالاك دەکرێت •**")
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await userbot.join_chat(invitelink)
                    join = True
                    await m.edit(f"**● ꒐ یاریدەدەر {user.mention} جۆین بوو •**\n**وە بۆت چالاککرا لە گرووپ دەتوانی گۆرانی لێ بدەیت •**")
                except UserAlreadyParticipant:
                    join = True
                except Exception as e:
                    await client.send_message(chat_id, f"**⎆┊ هەڵەیەک ڕوویدا، دواتر هەوڵبدەرەوە•\n⎆┊ {GROUP} : یان لێرەوە پەیوەندی بکە •**", reply_to_message_id=message_id)
        return join        

async def join_call(
        client,
        message_id,
        chat_id,
        bot_username,
        file_path,
        link,
        vid: Union[bool, str] = None):
        userbot = await get_userbot(bot_username)
        Done = None
        try:
          call = await get_call(bot_username)
        except:
          return Done
        file_path = file_path
        stream = (MediaStream(file_path, audio_parameters=AudioQuality.HIGH, video_parameters=VideoQuality.HD_720p) if vid else MediaStream(file_path, audio_parameters=AudioQuality.HIGH, video_flags=MediaStream.IGNORE,))
        try:
            await call.join_group_call(chat_id, stream)
            Done = True
        except NoActiveGroupCall:
                 h = await join_assistant(client, chat_id, message_id, userbot, file_path)
                 if h:
                  try:
                   await call.join_group_call(chat_id, stream)
                   Done = True
                  except Exception:
                      await client.send_message(chat_id, "**⎆┊ سەرەتا تێل بکەوە 🧑🏻‍💻•**", reply_to_message_id=message_id)
        except AlreadyJoinedError:
             await client.send_message(chat_id, "**⎆┊ دووبارە تێلەکە بکەرەوە •**", reply_to_message_id=message_id)
        except TelegramServerError:
             await client.send_message(chat_id, "**⎆┊ دووبارە تێلەکە بکەرەوە •**", reply_to_message_id=message_id)
        except Exception as a:
            print(a)
            return Done
        return Done

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


async def logs(bot_username, client, message):
  try:
   if await get_logger_mode(bot_username) == "OFF":
     return
   logger = await get_logger(bot_username)
   log = LOGS
   if message.chat.type == ChatType.CHANNEL:
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     name = f"{message.author_signature}" if message.author_signature else chat
     text = f"**زانیاری پەخشکردن**\n\n**گرووپ : {chat}**\n**ئایدی گرووپ : {message.chat.id}**\n**یوزەری بەکار‌هێنەر : {name}**\n\n**پەخشکراو : {message.text}**"
   else:
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     user = f"یوزەری بەکار‌هێنەر : @{message.from_user.username}" if message.from_user.username else f"ئـایدی بەکار‌هێنەر : {message.from_user.id}"
     text = f"**زانیاری پەخشکردن**\n\n**گرووپ : {chat}**\n**ئایدی گرووپ : {message.chat.id}**\n**ناوی بەکار‌هێنەر : {message.from_user.mention}**\n**{user}**\n\n**پەخشکراو : {message.text}**"
   await client.send_message(logger, text=text, disable_web_page_preview=True)
   return await man.send_message(log, text=f"[ @{bot_username} ]\n{text}", disable_web_page_preview=True)
  except:
    pass

@Client.on_message(filters.video_chat_started)
async def brah(client: Client, message):
    await message.reply("**• ئەدمین تێلی کردەوە ⎋**")

@Client.on_message(filters.video_chat_ended)
async def brah2(client: Client, message):
    await message.reply("**• ئەدمین تێلی داخست ⎋**")

@Client.on_message(filters.video_chat_members_invited)
async def fuckoff(client: Client, message):
    text = f"**تۆی {message.from_user.mention} ئەزیز\n• بانگێشتکرایی : **"
    x = 0
    for user in m.video_chat_members_invited.users:
        try:
            text += f"**{user.first_name} **"
            x += 1
        except Exception:
            pass
    try:
        await m.reply(f"**{text} \n🌚💕️**", reply_to_message_id=m.message_id)
    except:
        pass
      
@Client.on_message(filters.command(["/play", "play", "/vplay", "gorani", "پ ئەلینا", "پلەی", "ڤیدیو","سوڕەت"], ""))
async def play(client: Client, message):
  if await joinch(message):
            return
  ALINA = message
  bot = client.me
  bot_username = client.me.username
  dev = await get_dev(bot.username)
  devname = await get_dev_name(client, bot.username)
  chat_id = message.chat.id
  user_id = message.from_user.id if message.from_user else "Hawaall"
  message_id = message.id 
  gr = await get_group(bot_username)
  ch = await get_channel(bot_username)
  button = [[InlineKeyboardButton(text="𝗘𝗻𝗱 🎸", callback_data=f"stop"), InlineKeyboardButton(text="𝗥𝗲𝘀𝘂𝗺𝗲 🎸", callback_data=f"resume"), InlineKeyboardButton(text="𝗣𝗮𝘂𝘀𝗲 🎸", callback_data=f"pause")], [InlineKeyboardButton(text="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 💸•", url=f"{ch}"), InlineKeyboardButton(text="𝗚𝗿𝗼𝘂𝗽 💸•", url=f"{gr}")], [InlineKeyboardButton(f"{devname} 💸•", user_id=f"{dev}")], [InlineKeyboardButton(text="زیادم بکە بۆ گرووپ یان کەناڵت ⚡️•", url=f"https://t.me/{bot_username}?startgroup=True")]]
  if message.chat.type == ChatType.PRIVATE:
       return await message.reply_text("**⎆┊ بەداخەوە لێرە ناتوانی پەخش بکەیت 💎•\n⎆┊ بۆتەکە زیاد بکە بۆ گرووپەکەت بۆ ئەوەی گۆرانی  پەخش بکەیت 💎•**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"⌯ زیادم بکە بۆ گرووپت ⚡•", url=f"https://t.me/{bot_username}?startgroup=True")]]))
  if message.sender_chat:
     if not message.chat.type == ChatType.CHANNEL:
      return await message.reply_text("**⎆┊ تەنها دەتوانیت بە ئەکاونتی خۆت پەخشی بکەیت •**")
  if not len(message.command) == 1:
    rep = await message.reply_text("**⎆┊ کەمێك چاوەڕێ بکە پەخشدەکرێت 🎸•**")
  try:
          call = await get_call(bot_username)
  except:
          await remove_active(bot_username, chat_id)
  try:
       await call.get_call(message.chat.id)
  except pytgcalls.exceptions.GroupCallNotFound:
       await remove_active(bot_username, chat_id)
  if not message.reply_to_message:
     if len(message.command) == 1:
      if message.chat.type == ChatType.CHANNEL:
        return await message.reply_text("**⎆┊ شتێك بنووسە تاوەکو پەخشی بکەم 🎸•**")
      try:
       name = await client.ask(message.chat.id, text="**⎆┊ ناو یان لینکی گۆرانی بنێرە تا پەخشی بکەم 🎸•**", reply_to_message_id=message.id, filters=filters.user(message.from_user.id), timeout=200)
       name = name.text
       rep = await message.reply_text("**⎆┊ کەمێك چاوەڕێ بکە پەخشدەکرێت 🎸•**")
      except:
       return
     else:
       name = message.text.split(None, 1)[1]
     try:
      results = VideosSearch(name, limit=1)
     except Exception:
      return await rep.edit("**⎆┊ شکستی هێنا هیچ شتێك نەدۆزرایەوە 🎸•**")
     for result in (await results.next())["result"]:
         title = result["title"]
         duration = result["duration"]
         videoid = result["id"]
         yturl = result["link"]
         thumbnail = result["thumbnails"][0]["url"].split("?")[0]
     if "v" in message.command[0] or "ڤ" in message.command[0]:
       vid = True
     else:
       vid = None
     await rep.edit("**⎆┊ کەمێك چاوەڕێ بکە پەخشدەکرێت 💎•**")
     results = YoutubeSearch(name, max_results=5).to_dict()
     link = f"https://youtube.com{results[0]['url_suffix']}"
     if await is_served_call(client, message.chat.id):
         chat_id = message.chat.id
         title = title.title()
         file_path = None
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         chat = f"{bot_username}{chat_id}"
         position = len(db.get(chat)) - 1
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if ALINA.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
          elif message.chat.photo:
           photo_id = message.chat.photo.big_file_id
           photo = await client.download_media(photo_id)
          else:
           ahmed = await client.get_chat("Hawaall")
           ahmedphoto = ahmed.photo.big_file_id
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else:
          ahmed = await client.get_chat("Hawaall")
          ahmedphoto = ahmed.photo.big_file_id
          photo = await client.download_media(ahmedphoto)
         photo = await gen_thumb(videoid, photo)
         await message.reply_photo(photo=photo, caption=f"**⭓ᴍᴜˢɪᴄ✘ᴀʟɪɴᴀ ᴘʟᴀʏʟɪsᴛ : {position} 🎻\n\n╮◉ ناونیشان : {title[:18]}\n│᚜⦿ ماوەکەی : {duration} ⌚\n╯◉ لەلایەن : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     else:
         chat_id = message.chat.id
         title = title.title()
         await add_active_chat(chat_id)
         await add_served_call(client, chat_id)
         if vid:
           await add_active_video_chat(chat_id)
         file_path = await download(bot_username, link, vid)
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
         if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if ALINA.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
          elif message.chat.photo:
           photo_id = message.chat.photo.big_file_id
           photo = await client.download_media(photo_id)
          else:
           ahmed = await client.get_chat("Hawaall")
           ahmedphoto = ahmed.photo.big_file_id
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else:
          ahmed = await client.get_chat("Hawaall")
          ahmedphoto = ahmed.photo.big_file_id
          photo = await client.download_media(ahmedphoto)
         photo = await gen_thumb(videoid, photo)
         await message.reply_photo(photo=photo, caption=f"**⭓ᴍᴜˢɪᴄ✘ᴀʟɪɴᴀ 🎻\n\n╮◉ ناونیشان : {title}\n│᚜⦿ ماوەکەی : {duration} ⌚\n╯◉ لەلایەن : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     await rep.delete()
  else:
       if not message.reply_to_message.media:
         return
       rep = await message.reply_text("**⎆┊ چاوەڕێ بکە پەخشدەکرێت 🎸•**") 
       photo = "Uploaded to https://graph.org/file/ffb9ba387b686493f06cb.jpg"
       if message.reply_to_message.video or message.reply_to_message.document:
           vid = True
       else:
           vid = None
       file_path = await message.reply_to_message.download()
       if message.reply_to_message.audio:
         file_name = message.reply_to_message.audio
       elif message.reply_to_message.voice:
         file_name = message.reply_to_message.voice
       elif message.reply_to_message.video:
         file_name = message.reply_to_message.video
       else:
         file_name = message.reply_to_message.document
       title = file_name.file_name
       duration = seconds_to_min(file_name.duration)
       link = None
       if await is_served_call(client, message.chat.id):
         chat_id = message.chat.id
         videoid = None
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         chat = f"{bot_username}{chat_id}"
         position = len(db.get(chat)) - 1
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if ALINA.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         await message.reply_photo(photo=photo, caption=f"**⭓ᴍᴜˢɪᴄ✘ᴀʟɪɴᴀ ᴘʟᴀʏʟɪsᴛ : {position} 🎻\n\n╮◉ ناونیشان : {title[:18]}\n│᚜⦿ ماوەکەی : {duration} ⌚\n╯◉ لەلایەن : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
       else:
         chat_id = message.chat.id
         videoid = None
         await add_active_chat(chat_id)
         await add_served_call(client, chat_id)
         if vid:
            await add_active_video_chat(chat_id)
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
         if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if ALINA.views else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         await message.reply_photo(photo=photo, caption=f"**⭓ᴍᴜˢɪᴄ✘ᴀʟɪɴᴀ 🎻\n\n╮◉ ناونیشان : {title}\n│᚜⦿ ماوەکەی : {duration} ⌚\n╯◉ لەلایەن : {requester}**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
  try:
     os.remove(file_path)
     os.remove(photo)
  except:
     pass
  await rep.delete()
