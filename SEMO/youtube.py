from pyrogram import Client, filters as ay
from yt_dlp import YoutubeDL
from requests import get
from youtube_search import YoutubeSearch
import os, wget
from pyrogram.types import (
   InlineKeyboardMarkup,
   InlineKeyboardButton,
   InlineQuery,
   InlineQueryResultArticle,
   InputTextMessageContent,
)



@Client.on_message(ay.command(["/song", "/video","/yt", "داگرتن", "/youtube", "/download", "دونلۆد"], ""))
async def start(client, message):
   await message.reply_text(
      "**👋🏻 ꒐ بەخێربێی\n🎻 ꒐ بۆ بەشی داگرتنی گۆرانی و ڤیدیۆ\n⚡ ꒐ بە بەرزترین کوالێتی\n🧑🏻‍💻 ꒐ لینکی یوتوب بنێرە**",
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿", url=f"https://t.me/IQ7amo"),
            ],[
               InlineKeyboardButton("˹s ᴏ ᴜ ꝛ ᴄ ᴇ ✗ ᴀ ʟ ɪ ɴ ᴀ˼", url=f"https://t.me/MGIMT"),
            ]
         ]
      )
   )

@Client.on_message(ay.regex(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"))
async def ytdl(client, message):
   await message.reply_text(
      f"**🎬 : {message.text} **",disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
         [
            [
               InlineKeyboardButton("دەنـگ ⎮ گۆرانـی 🎻", callback_data="audio"),
            ],[
               InlineKeyboardButton("ڤـیـدیـۆ 🎥", callback_data="video"),
            ]
         ]
      )
   )

@Client.on_callback_query(ay.regex("video"))
async def VideoDownLoad(client, callback_query):
   await callback_query.edit_message_text("**کەمێك چاوەڕێ بکە ڤیدۆ دادەگرم...❄⚡**")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(video) as ytdl:
         await callback_query.edit_message_text("**دادەبەزێت...**")
         ytdl_data = ytdl.extract_info(url, download=True)
         video_file = ytdl.prepare_filename(ytdl_data)
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("**...**")
   await client.send_video(
            callback_query.message.chat.id,
            video=video_file,
            duration=int(ytdl_data["duration"]),
            file_name=str(ytdl_data["title"]),
            supports_streaming=True,
            caption=f"[{ytdl_data['title']}]({url})",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("˹s ᴏ ᴜ ꝛ ᴄ ᴇ ✗ ᴀ ʟ ɪ ɴ ᴀ˼", url="https://t.me/mgimt")]]))
   os.remove(video_file)

@Client.on_callback_query(ay.regex("audio"))
async def AudioDownLoad(client, callback_query):
   await callback_query.edit_message_text("**کەمێك چاوەڕێ بکە گۆرانی دادەگرم...❄⚡**")
   try:
      url = callback_query.message.text.split(' : ',1)[1]
      with YoutubeDL(audio) as ytdl:
         await callback_query.edit_message_text("**دادەبەزێت...**")
         ytdl_data = ytdl.extract_info(url, download=True)
         audio_file = ytdl.prepare_filename(ytdl_data)
         thumb = wget.download(f"https://img.youtube.com/vi/{ytdl_data['id']}/hqdefault.jpg")
   except Exception as e:
      await client.send_message(chat_id=Sudo_id,text=e)
      return await callback_query.edit_message_text(e)
   await callback_query.edit_message_text("**چاوەڕێ بکە**")
   await client.send_audio(
      callback_query.message.chat.id,
      audio=audio_file,
      duration=int(ytdl_data["duration"]),
      title=str(ytdl_data["title"]),
      performer=str(ytdl_data["uploader"]),
      file_name=str(ytdl_data["title"]),
      thumb=thumb,
      caption=f"[{ytdl_data['title']}]({url})",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("˹s ᴏ ᴜ ꝛ ᴄ ᴇ ✗ ᴀ ʟ ɪ ɴ ᴀ˼", url="https://t.me/mgimt")]]))
   os.remove(audio_file)
   os.remove(thumb)


@Client.on_message(ay.command(["/search", "گەڕان", "گەران"],None))
async def search(client, message):
    try:
        query = message.text.split(None, 1)[1]
        if not query:
            await message.reply_text("**فەرمان بەکاربێنە بەم جۆرە ( گەڕان + وشە )**")
            return

        m = await message.reply_text("**کەمێك چاوەڕێ بکە دەگەڕێم...❄⚡**")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"👤 {results[i]['title']}\n"
            text += f"🕑 {results[i]['duration']}\n"
            text += f"👁 {results[i]['views']}\n"
            text += f"🌐 {results[i]['channel']}\n"
            text += f"🔗 https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("˹s ᴏ ᴜ ꝛ ᴄ ᴇ ✗ ᴀ ʟ ɪ ɴ ᴀ˼", url="https://t.me/mgimt")]]), disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))

@Client.on_inline_query()
async def inline(client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="جۆری ناوی گۆرانی",
            switch_pm_parameter="help",
            cache_time=0,
        )
    else:
        results = YoutubeSearch(search_query).to_dict()
        for result in results:
         answers.append(
               InlineQueryResultArticle(
                  title=result["title"],
                  description="{}, {} views.".format(
                     result["duration"], result["views"]
                  ),
                  input_message_content=InputTextMessageContent(
                     "🔗 https://www.youtube.com/watch?v={}".format(result["id"])
                  ),
                  thumb_url=result["thumbnails"][0],
               )
         )
        
        try:
            await query.answer(results=answers, cache_time=0)
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: search timed out",
                switch_pm_parameter="",
            )
            
video = {"format": "best","keepvideo": True,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.%(ext)s","quite": True}
audio = {"format": "bestaudio","keepvideo": False,"prefer_ffmpeg": False,"geo_bypass": True,"outtmpl": "%(title)s.mp3","quite": True}
