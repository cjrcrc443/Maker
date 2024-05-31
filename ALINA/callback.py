from pyrogram import filters, Client 
from config import OWNER_NAME, GROUP
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from ALINA.Data import get_dev, get_group, get_channel, get_dev_name


@Client.on_callback_query(filters.regex("kurdish"))
async def kurdish(client: Client, query: CallbackQuery):
    bot = client.me
    ch = await get_channel(bot.username)
    gr = await get_group(bot.username)
    dev = await get_dev(bot.username)
    devname = await get_dev_name(client, bot.username)
    await query.answer("لیستی سەرەکی")
    await query.edit_message_text(f"**👋🏻 ꒐ بەخێربێی ئەزیزم {query.from_user.mention} **\n\n**● ꒐ من بۆتێکم کە دەتوانم گۆرانی لێبدەم**\n**● ꒐ زیادم بکە بۆ گرووپت یان کەناڵت**\n**● ꒐ خێرایە کاتێك چالاکت کرد یاریدەدەر جۆینەکات**\n**● ꒐ لە کاتی هەبوونی هەر کێشەیەك سەردانی گرووپ بکە**\n**🍻 ꒐ گرووپ : {gr} **\n**🍻 ꒐ دووگمەکانی خوارەوە بەکاربێنە**\n**👾 ꒐ گەشەپێدراوە لەلایەن : {OWNER_NAME}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝄞 زیادم بکە بۆ گرووپەکەت 𝄞",
                        url=f"https://t.me/{bot.username}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton(f"{devname}", user_id=f"{dev}")],
                [
                    InlineKeyboardButton("𝄞 چۆنیەتی کارکردن 𝄞", callback_data="bcmds"),
                    InlineKeyboardButton("𝄞 چۆنیەتی چالاککردن 𝄞", callback_data="bhowtouse"),
                ],
                [
                    InlineKeyboardButton(
                        "گرووپی بۆت", url=f"{gr}"
                    ),
                    InlineKeyboardButton(
                        "کەناڵی بۆت", url=f"{ch}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "𝄞 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝘼𝙒𝘼𝙇 𝄞",
                        url=f"https://t.me/Haawall"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex("english"))
async def english(client: Client, query: CallbackQuery):
    bot = client.me
    ch = await get_channel(bot.username)
    gr = await get_group(bot.username)
    dev = await get_dev(bot.username)
    devname = await get_dev_name(client, bot.username)
    await query.answer("𝖧𝗈𝗆𝖾 𝖲𝗍𝖺𝗋𝗍")
    await query.edit_message_text(f"**👋🏻 ꒐ 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖽𝖾𝖺𝗋 {query.from_user.mention}\n\n● ꒐ 𝖨'𝗆 𝖺 𝖻𝗈𝗍 𝗍𝗁𝖺𝗍 𝖼𝖺𝗇 𝗉𝗅𝖺𝗒 𝗌𝗈𝗇𝗀𝗌\n● ꒐ 𝖠𝖽𝖽 𝗆𝖾 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝗈𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅\n● ꒐ 𝖨𝗍'𝗌 𝖿𝖺𝗌𝗍, 𝗍𝗁𝖾 𝖺𝗌𝗌𝗂𝗌𝗍𝖺𝗇𝗍 𝗃𝗈𝗂𝗇𝗌 𝗐𝗁𝖾𝗇 𝗒𝗈𝗎 𝖺𝖼𝗍𝗂𝗏𝖺𝗍𝖾 𝗂𝗍\n● ꒐ 𝖵𝗂𝗌𝗂𝗍 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉 𝗂𝖿 𝗒𝗈𝗎 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝗋𝗈𝖻𝗅𝖾𝗆𝗌\n🍻 ꒐ 𝖦𝗋𝗈𝗎𝗉 : {gr} \n🍻 ꒐ 𝖴𝗌𝖾 𝗍𝗁𝖾 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝖻𝖾𝗅𝗈𝗐\n👾 ꒐ 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝖽 𝖡𝗒 : {OWNER_NAME}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝄞 𝖠𝖽𝖽 𝗆𝖾 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝄞",
                        url=f"https://t.me/{bot.username}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton(f"{devname}", user_id=f"{dev}")],
                [
                    InlineKeyboardButton("𝄞 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝄞", callback_data="cbcmds"),
                    InlineKeyboardButton("𝄞 𝖡𝖺𝗌𝗂𝖼 𝖦𝗎𝗂𝖽𝖾 𝄞", callback_data="cbhowtouse"),
                ],
                [
                    InlineKeyboardButton(
                        "𝖡𝗈𝗍'𝗌 𝖦𝗋𝗈𝗎𝗉", url=f"{gr}"
                    ),
                    InlineKeyboardButton(
                        "𝖡𝗈𝗍'𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅", url=f"{ch}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "𝄞 𝙎𝙊𝙐𝙍𝘾𝞝 𝙃𝘼𝙒𝘼𝙇 𝄞",
                        url=f"https://t.me/Haawall"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.answer("𝖡𝖺𝗌𝗂𝖼 𝖢𝗈𝗆𝗆𝖺𝗇𝖽")
    await query.edit_message_text(
        f"""**𝄞 ꒐ 𝖡𝖺𝗌𝗂𝖼 𝖦𝗎𝗂𝖽𝖾 𝖿𝗈𝗋 𝗎𝗌𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 :
        
1.) 𝖥𝗂𝗋𝗌𝗍, 𝖺𝖽𝖽 𝗆𝖾 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉.
2.) 𝖳𝗁𝖾𝗇, 𝗉𝗋𝗈𝗆𝗈𝗍𝖾 𝗆𝖾 𝖺𝗌 𝖺𝖽𝗆𝗂𝗇𝗂𝗌𝗍𝗋𝖺𝗍𝗈𝗋 𝖺𝗇𝖽 𝗀𝗂𝗏𝖾 𝖺𝗅𝗅 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇𝗌 𝖾𝗑𝖼𝖾𝗉𝗍 𝖠𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌 𝖠𝖽𝗆𝗂𝗇.
3.) 𝖠𝖿𝗍𝖾𝗋 𝗉𝗋𝗈𝗆𝗈𝗍𝗂𝗇𝗀 𝗆𝖾, 𝗍𝗒𝗉𝖾 /𝗋𝖾𝗅𝗈𝖺𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉 𝗍𝗈 𝗋𝖾𝖿𝗋𝖾𝗌𝗁 𝗍𝗁𝖾 𝖺𝖽𝗆𝗂𝗇 𝖽𝖺𝗍𝖺.
4.) 𝖳𝗎𝗋𝗇 𝗈𝗇 𝗍𝗁𝖾 𝗏𝗂𝖽𝖾𝗈 𝖼𝗁𝖺𝗍 𝖿𝗂𝗋𝗌𝗍 𝖻𝖾𝖿𝗈𝗋𝖾 𝗌𝗍𝖺𝗋𝗍 𝗍𝗈 𝗉𝗅𝖺𝗒 𝗏𝗂𝖽𝖾𝗈/𝗆𝗎𝗌𝗂𝖼.
5.) 𝖲𝗈𝗆𝖾𝗍𝗂𝗆𝖾𝗌, 𝗋𝖾𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗍𝗁𝖾 𝖻𝗈𝗍 𝖻𝗒 𝗎𝗌𝗂𝗇𝗀 /𝗋𝖾𝗅𝗈𝖺𝖽 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝖼𝖺𝗇 𝗁𝖾𝗅𝗉 𝗒𝗈𝗎 𝗍𝗈 𝖿𝗂𝗑 𝗌𝗈𝗆𝖾 𝗉𝗋𝗈𝖻𝗅𝖾𝗆.
📌 𝖨𝖿 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋𝖻𝗈𝗍 𝗇𝗈𝗍 𝗃𝗈𝗂𝗇𝖾𝖽 𝗍𝗈 𝗏𝗂𝖽𝖾𝗈 𝖼𝗁𝖺𝗍, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗂𝖿 𝗍𝗁𝖾 𝗏𝗂𝖽𝖾𝗈 𝖼𝗁𝖺𝗍 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗍𝗎𝗋𝗇𝖾𝖽 𝗈𝗇.
💡 𝖨𝖿 𝗒𝗈𝗎 𝗁𝖺𝗏𝖾 𝖺 𝖿𝗈𝗅𝗅𝗈𝗐-𝗎𝗉 𝗊𝗎𝖾𝗌𝗍𝗂𝗈𝗇𝗌 𝖺𝖻𝗈𝗎𝗍 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍, 𝗒𝗈𝗎 𝖼𝖺𝗇 𝗍𝖾𝗅𝗅 𝗂𝗍 𝗈𝗇 𝗆𝗒 𝗌𝗎𝗉𝗉𝗈𝗋𝗍 𝖼𝗁𝖺𝗍 𝗁𝖾𝗋𝖾 : {GROUP}
👾 ꒐ 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 𝖡𝗒 : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• 𝖡𝖺𝖼𝗄 •", callback_data="english")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("𝖬𝖾𝗇𝗎 𝖢𝗈𝗆𝗆𝖺𝗇𝖽")
    await query.edit_message_text(
        f"""**👋🏻 ꒐ [{query.from_user.mention}](tg://user?id={query.message.from_user.id})\n**● ꒐ 𝖯𝗋𝖾𝗌𝗌 𝗍𝗁𝖾 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝗍𝗈 𝗋𝖾𝖺𝖽 𝗍𝗁𝖾 𝖾𝗑𝗉𝗅𝖺𝗇𝖺𝗍𝗂𝗈𝗇 𝖺𝗇𝖽 𝗌𝖾𝖾 𝗍𝗁𝖾 𝗅𝗂𝗌𝗍 𝗈𝖿 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌\n👾 ꒐ 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 𝖡𝗒 : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝖠𝖽𝗆𝗂𝗇 𝖢𝗈𝗆𝗆𝖺𝗇𝖽", callback_data="cbadmin"),
                    InlineKeyboardButton("𝖡𝖺𝗌𝗂𝖼 𝖢𝗈𝗆𝗆𝖺𝗇𝖽", callback_data="cbbasic"),
                ],[
                    InlineKeyboardButton("• 𝖡𝖺𝖼𝗄 •", callback_data="english")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.answer("𝖡𝖺𝗌𝗂𝖼 𝖢𝗈𝗆𝗆𝖺𝗇𝖽")
    await query.edit_message_text(
        f"""**𝄞 ꒐ 𝗁𝖾𝗋𝖾 𝗂𝗌 𝗍𝗁𝖾 𝖻𝖺𝗌𝗂𝖼 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌 :
» /play (𝗌𝗈𝗇𝗀 𝗇𝖺𝗆𝖾/𝗅𝗂𝗇𝗄) - 𝗉𝗅𝖺𝗒 𝗆𝗎𝗌𝗂𝖼 𝗈𝗇 𝗏𝗂𝖽𝖾𝗈 𝖼𝗁𝖺𝗍
» /vplay (𝗏𝗂𝖽𝖾𝗈 𝗇𝖺𝗆𝖾/𝗅𝗂𝗇𝗄) - 𝗉𝗅𝖺𝗒 𝗏𝗂𝖽𝖾𝗈 𝗈𝗇 𝗏𝗂𝖽𝖾𝗈 𝖼𝗁𝖺𝗍
» /video (𝗊𝗎𝖾𝗋𝗒) - 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝗏𝗂𝖽𝖾𝗈 𝖿𝗋𝗈𝗆 𝗒𝗈𝗎𝗍𝗎𝖻𝖾
» /song (𝗊𝗎𝖾𝗋𝗒) - 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝗌𝗈𝗇𝗀 𝖿𝗋𝗈𝗆 𝗒𝗈𝗎𝗍𝗎𝖻𝖾
» /search (𝗊𝗎𝖾𝗋𝗒) - 𝗌𝖾𝖺𝗋𝖼𝗁 𝖺 𝗒𝗈𝗎𝗍𝗎𝖻𝖾 𝗏𝗂𝖽𝖾𝗈 𝗅𝗂𝗇𝗄
» /ping - 𝗌𝗁𝗈𝗐 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗉𝗂𝗇𝗀 𝗌𝗍𝖺𝗍𝗎𝗌
» /alive - 𝗌𝗁𝗈𝗐 𝗍𝗁𝖾 𝖻𝗈𝗍 𝖺𝗅𝗂𝗏𝖾 𝗂𝗇𝖿𝗈 (𝗂𝗇 𝗀𝗋𝗈𝗎𝗉)
👾 ꒐ 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 𝖡𝗒 : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• 𝖡𝖺𝖼𝗄 •", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.answer("𝖠𝖽𝗆𝗂𝗇 𝖢𝗈𝗆𝗆𝖺𝗇𝖽")
    await query.edit_message_text(
        f"""**𝄞 ꒐ 𝗁𝖾𝗋𝖾 𝗂𝗌 𝗍𝗁𝖾 𝖺𝖽𝗆𝗂𝗇 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌 :
» /pause - 𝗉𝖺𝗎𝗌𝖾 𝗍𝗁𝖾 𝗌𝗍𝗋𝖾𝖺𝗆
» /resume - 𝗋𝖾𝗌𝗎𝗆𝖾 𝗍𝗁𝖾 𝗌𝗍𝗋𝖾𝖺𝗆
» /skip - 𝗌𝗐𝗂𝗍𝖼𝗁 𝗍𝗈 𝗇𝖾𝗑𝗍 𝗌𝗍𝗋𝖾𝖺𝗆
» /stop - 𝗌𝗍𝗈𝗉 𝗍𝗁𝖾 𝗌𝗍𝗋𝖾𝖺𝗆𝗂𝗇𝗀
» /loop - 𝗅𝗈𝗈𝗉 𝗍𝗁𝖾 𝗌𝗍𝗋𝖾𝖺𝗆𝗂𝗇𝗀
👾 ꒐ 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 𝖡𝗒 : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• 𝖡𝖺𝖼𝗄 •", callback_data="cbcmds")]]
        ),
    )



@Client.on_callback_query(filters.regex("bhowtouse"))
async def acbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**𝄞 ꒐ ڕێنمایی بنەڕەتی بۆ بەکارهێنانی ئەم بۆتە :
1.) سەرەتا من زیاد بکە بۆ گرووپەکەت.
2.) پاشان، پلەم بەرز بکەرەوە وەک بەڕێوەبەر و هەموو ڕۆڵەکانم پێ بدە جگە لە ئەدمینی بێناو.
3.) دوای کە بوومە ئەدمین، لە گرووپ بنووسە /reload بۆ نوێکردنەوەی داتای ئەدمین.
4.) سەرەتا تێل بکەوە پێش ئەوەی دەست بکەیت بە لێدانی ڤیدیۆیان گۆرانی.
5.) هەندێک جار، دووبارە بارکردنی بۆتەکە بە بەکارهێنانی فرمانی /reload دەتوانێت یارمەتیت بدات بۆ چارەسەرکردنی هەندێك کێشە.
📌 ئەگەر یاریدەدە بەشداری تێلی نەکرد، دڵنیابە لەوەی کە پێشتر تێڵ کراوەتەوە.
💡 ئەگەر پرسیارت هەیە لەسەر ئەم بۆتە، دەتوانیت لە گرووپی پشتگیری مندا بیکەیت : {GROUP} .
👾 ꒐ گەشەپێدراوە لەلایەن : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• گـەڕانـەوە •", callback_data="kurdish")]]
        ),
    )


@Client.on_callback_query(filters.regex("bcmds"))
async def acbcmds(_, query: CallbackQuery):
    await query.answer("فەرمانەکان")
    await query.edit_message_text(
        f"""**👋🏻 ꒐ [{query.from_user.mention}](tg://user?id={query.message.from_user.id})\n**● ꒐ بۆ خوێندنەوەی ڕوونکردنەوە و بینینی لیستی فەرمانە بەردەستەکان، دوگمەی خوارەوە داگرە\n👾 ꒐ گەشەپێدراوە لەلایەن : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("فەرمانی پەخشکردن", callback_data="bbasic"),
                    InlineKeyboardButton("فەرمانی ئەدمین", callback_data="badmin"),
                ],[
                    InlineKeyboardButton("• گـەڕانـەوە •", callback_data="kurdish")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("bbasic"))
async def acbbasic(_, query: CallbackQuery):
    await query.answer("فەرمانی پەخشکردن")
    await query.edit_message_text(
        f"""**𝄞 ꒐ فەرمانی پەخشکردن :
        
» /play یان پلەی - بۆ پەخشکردنی گۆرانی  
» /vplay یان ڤیدیو - بۆ پەخشکردنی ڤیدیۆ
» /search یان گەڕان - بۆ گەڕانی گۆرانی لە یوتوب
» /video + ناوی ڤیدیۆ - بۆ داگرتنی ڤیدیۆ
» /song + ناوی گۆرانی - بۆ داگرتنی گۆرانی
» /ping - بۆ پیشاندانی خێرایی
» /alive - بۆ پیشاندانی زانیاری بۆت 
👾 ꒐ گەشەپێدراوە لەلایەن : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• گـەڕانـەوە •", callback_data="bcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("badmin"))
async def acbadmin(_, query: CallbackQuery):
    await query.answer("فەرمانی ئەدمین")
    await query.edit_message_text(
        f"""**𝄞 ꒐ فەرمانەکانی کۆنترۆڵکردن بۆ ئەدمینەکان :

 » /pause - وەستاندنی پەخشکردن بۆ ماوەیەکی کاتی
 » /resume - بۆ تەواوکردنی پەخشکردن کاتێ وەستاوە
 » /skip - بۆ تێپەڕاندنی پەخشکردنی ئێستا
 » /stop - بۆ وەستاندنی پەخشکردنی ئێستا
 » /loop - بۆ دووبارەکردنەوەی پەخشکردنی ئێستا
 👾 ꒐ گەشەپێدراوە لەلایەن : {OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• گـەڕانـەوە •", callback_data="bcmds")]]
        ),
    )
