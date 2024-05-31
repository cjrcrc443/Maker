import asyncio
from config import OWNER, OWNER_NAME, VIDEO
from pyrogram import Client, filters
from ALINA.info import (remove_active, is_served_call, joinch)
from ALINA.Data import (get_call, get_dev, get_group, get_channel)
from ALINA.info import (add, db, download, gen_thumb)
from pytgcalls import PyTgCalls
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls.types import (
    MediaStream,
    AudioQuality,
    VideoQuality,
    Update,
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery

@Client.on_callback_query(
    filters.regex(pattern=r"^(pause|skip|stop|resume)$")
)
async def admin_risghts(client: Client, CallbackQuery):
  try:
    a = await client.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
     if not CallbackQuery.from_user.id == dev:
      if not CallbackQuery.from_user.username in OWNER:
        return await CallbackQuery.answer("پێویستە ئەدمین بیت بۆ کردنی ئەم کارە !", show_alert=True)
    command = CallbackQuery.matches[0].group(1)
    chat_id = CallbackQuery.message.chat.id
    if not await is_served_call(client, chat_id):
        return await CallbackQuery.answer("هیچ پەخشکردنێك بوونی نییە لە ئێستادا .", show_alert=True)
    call = await get_call(bot_username)
    chat_id = CallbackQuery.message.chat.id
    if command == "pause":
        await call.pause_stream(chat_id)
        await CallbackQuery.answer("پەخشکردن وەستا بۆ ماوەیەکی کاتی ☕🍀", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **پەخشکردن وەستا بۆماوەیەکی کاتی لەلایەن**")
    if command == "resume":
        await call.resume_stream(chat_id)
        await CallbackQuery.answer("پەخشکردن دەستی پێکردەوە ☕🍀", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **پەخشکردن دەستی پێکردەوە لەلایەن**")
    if command == "stop":
        try:
         await call.leave_group_call(chat_id)
        except:
          pass
        await remove_active(bot_username, chat_id)
        await CallbackQuery.answer("بە سەرکەوتوویی پەخشکردن وەستا|ڕاگرترا ⚡", show_alert=True)
        await CallbackQuery.message.reply_text(f"{CallbackQuery.from_user.mention} **پەخشکردن وەستا|ڕاگرترا لەلایەن**")
  except:
     pass

@Client.on_message(filters.command(["/stop", "/end", "/skip", "/resume", "/pause", "/loop", "دواتر", "دەستپێکردنەوە", "سکیپ", "وەستان", "وەستانی کاتی", "وسبە", "دووبارەکردنەوە", "ڕاگرتن"], "") & ~filters.private)
async def admin_risght(client: Client, message):
  try:
    if await joinch(message):
            return
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if not message.chat.type == ChatType.CHANNEL:
     a = await client.get_chat_member(message.chat.id, message.from_user.id)
     if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
      if not message.from_user.id == dev:
       if not message.from_user.username in OWNER:
        return await message.reply_text("**پێویستە ئەدمین بیت بۆ کردنی ئەم کارە !**")
    command = message.command[0]
    chat_id = message.chat.id
    if not await is_served_call(client, chat_id):
        return await message.reply_text("**هیچ پەخشکردنێك بوونی نییە لە ئێستادا .**")
    call = await get_call(bot_username)
    chat_id = message.chat.id
    if command == "/pause" or command == "وەستانی کاتی":
        await call.pause_stream(chat_id)
        await message.reply_text(f"**پەخشکردن وەستا بۆ ماوەیەکی کاتی .♻️**")
    elif command == "/resume" or command == "دەستپێکردنەوە":
        await call.resume_stream(chat_id)
        await message.reply_text(f"**پەخشکردن دەست پێکردەوە .🚀**")
    elif command == "/stop" or command == "/end" or command == "وەستان" or command == "ڕاگرتن":
        try:
         await call.leave_group_call(chat_id)
        except:
         pass
        await remove_active(bot_username, chat_id)
        await message.reply_text(f"**پەخشکردن وەستا|ڕاگرترا .**")
    elif command == "دووبارەکردنەوە" or command == "/loop":
            if len(message.text) == 1:
               return await message.reply_text("**ژمارەی دووبارەکردنەوە بنووسه ..🖱️**")
            x = message.text.split(None, 1)[1]
            i = x
            if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
              x = i
              xx = f"{x} جار"
            elif x == "جار":
              x = 1
              xx = "یەك جار"
            elif x == "دوو جار":
              x = 2
              xx = "دوو جار"
            else:
              return await message.reply_text("**هەڵە ڕوویدا لە فەرمان ،**\n**فەرمان بەکاربێنە بەم شێوەیە « دووبارەکردنەوە 1**")
            chat = f"{bot_username}{chat_id}"
            check = db.get(chat)
            file_path = check[0]["file_path"]
            title = check[0]["title"]
            duration = check[0]["dur"]
            user_id = check[0]["user_id"]
            chat_id = check[0]["chat_id"]
            vid = check[0]["vid"]
            link = check[0]["link"]
            videoid = check[0]["videoid"]
            for i in range(x):
                file_path = file_path if file_path else None
                await add(chat_id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            await message.reply_text(f"**دووبارەکردنەوە چالاککرا {xx}**")
    elif command == "/skip" or command == "دواتر" or command == "سکیپ":
       chat = f"{bot_username}{chat_id}"
       check = db.get(chat)
       popped = check.pop(0)
       if not check:
         await call.leave_group_call(chat_id)
         await remove_active(bot_username, chat_id)
         return await message.reply_text("**پەخشکردنم وەستاند چونکە لیستی گۆرانی بەتاڵە 🎻.**")
       file = check[0]["file_path"]
       title = check[0]["title"]
       dur = check[0]["dur"]
       video = check[0]["vid"]
       videoid = check[0]["videoid"]
       user_id = check[0]["user_id"]
       link = check[0]["link"]
       if file:
         file_path = file
       else:     
         try:
            file_path = await download(bot_username, link, video)
         except:
            return client.send_message(chat_id, "**هەڵە ڕوویدا لە کاتی پەخشکردنی دواتر 🎻.**")
       stream = (MediaStream(file_path, audio_parameters=AudioQuality.HIGH, video_parameters=VideoQuality.HD_720p) if video else MediaStream(file_path, audio_parameters=AudioQuality.HIGH, video_flags=MediaStream.IGNORE,))
       try:
           await call.change_stream(chat_id, stream)
       except Exception:
            return await client.send_message(chat_id, "**هەڵە ڕوویدا لە کاتی پەخشکردنی دواتر 🎻.**")
       userx = await client.get_users(user_id)
       if videoid:
         if userx.photo:
            photo_id = userx.photo.big_file_id
         else:
            ahmed = await client.get_chat("Hawaall")
            photo_id = ahmed.photo.big_file_id
         photo = await client.download_media(photo_id)
         img = await gen_thumb(videoid, photo)
       else:
         img = VIDEO
       requester = userx.mention       
       gr = await get_group(bot_username)
       ch = await get_channel(bot_username)
       button = [[InlineKeyboardButton(text="END", callback_data=f"stop"), InlineKeyboardButton(text="RESUME", callback_data=f"resume"), InlineKeyboardButton(text="PAUSE", callback_data=f"pause")], [InlineKeyboardButton(text="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🌐", url=f"{ch}"), InlineKeyboardButton(text="𝗚𝗿𝗼𝘂𝗽 ♻️", url=f"{gr}")], [InlineKeyboardButton(text=f"{OWNER_NAME}", url="https://t.me/IQ7amo")], [InlineKeyboardButton(text="زیادم بکە بۆ گرووپ یان کەناڵت ⚡", url=f"https://t.me/{bot_username}?startgroup=True")]]
       await message.reply_photo(photo=img, caption=f"**⭓ᴍᴜˢɪᴄ✘ᴀʟɪɴᴀ 🎻\n\n╮◉ ناونیشان : {title}\n│᚜⦿ ماوەکەی : {duration} ⌚\n╯◉ لەلایەن : {requester}**", reply_markup=InlineKeyboardMarkup(button))
       try:
           os.remove(file_path)
           os.remove(img)
       except:
           pass
    else:
      await message.reply_text("**هەڵە لە بەکارهێنانی فەرمان**")
  except:
    pass
