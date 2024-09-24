import os
import random
from time import time

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from pyrogram import Client
from pyrogram import Client as app
from pyrogram import enums, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
)
from youtubesearchpython.__future__ import VideosSearch

from ALINA.Data import (
    get_bot_name,
    get_channel,
    get_channelsr,
    get_dev,
    get_dev_name,
    get_group,
    get_groupsr,
    get_userbot,
    set_bot_name,
    set_dev_user,
    set_video_source,
)
from ALINA.info import (
    add_served_chat,
    add_served_user,
    del_served_chat,
    get_served_chats,
    get_served_users,
    is_served_chat,
    is_served_user,
    joinch,
)
from config import OWNER, OWNER_NAME, VIDEO, user

joinandleft = [
    "https://graph.org/file/9340f44e4a181b18ac663.jpg",
    "https://graph.org/file/50037e072302b4eff55ba.jpg",
    "https://graph.org/file/39f39cf6c6c68170f6bf2.jpg",
    "https://graph.org/file/abf9931642773bc27ad7f.jpg",
    "https://graph.org/file/60764ec9d2b1fda50c2d1.jpg",
    "https://graph.org/file/a90c116b776c90d58f5e8.jpg",
    "https://graph.org/file/b2822e1b60e62caa43ceb.jpg",
    "https://graph.org/file/84998ca9871e231df0897.jpg",
    "https://graph.org/file/6c5493fd2f6c403486450.jpg",
    "https://graph.org/file/9dd91a4a794f15e5dadb3.jpg",
    "https://graph.org/file/0a2fb6e502f6c9b6a04ac.jpg",
    "https://graph.org/file/774380facd73524f27d26.jpg",
]

ahmed = "https://graph.org/file/3202937ba2792dfa8722f.jpg"


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_bot(client, username, photo):
    if os.path.isfile(f"{username}.png"):
        return f"{username}.png"
    users = len(await get_served_users(client))
    chats = len(await get_served_chats(client))
    url = f"https://www.youtube.com/watch?v=gKA2XFkJZhI"
    results = VideosSearch(url, limit=1)
    for result in (await results.next())["result"]:
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"thumb{username}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    youtube = Image.open(f"{photo}")
    Mostafa = Image.open(f"{photo}")
    image1 = changeImageSize(1280, 720, youtube)
    image2 = image1.convert("RGBA")
    background = image2.filter(filter=ImageFilter.BoxBlur(5))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.6)
    Xcenter = Mostafa.width / 2
    Ycenter = Mostafa.height / 2
    x1 = Xcenter - 250
    y1 = Ycenter - 250
    x2 = Xcenter + 250
    y2 = Ycenter + 250
    logo = Mostafa.crop((x1, y1, x2, y2))
    logo.thumbnail((520, 520), Image.ANTIALIAS)
    logo = ImageOps.expand(logo, border=15, fill="white")
    background.paste(logo, (50, 100))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("font2.ttf", 40)
    font2 = ImageFont.truetype("font2.ttf", 70)
    arial = ImageFont.truetype("font2.ttf", 30)
    name_font = ImageFont.truetype("font.ttf", 30)
    draw.text(
        (600, 150),
        "Music Player BoT",
        fill="white",
        stroke_width=2,
        stroke_fill="white",
        font=font2,
    )
    draw.text(
        (600, 340),
        f"Dev : Hawaall",
        fill="white",
        stroke_width=1,
        stroke_fill="white",
        font=font,
    )
    draw.text(
        (600, 280),
        f"Playing Music & Video",
        fill="white",
        stroke_width=1,
        stroke_fill="white",
        font=font,
    )

    draw.text(
        (600, 400),
        f"user : {users}",
        (255, 255, 255),
        font=arial,
    )
    draw.text(
        (600, 450),
        f"chats : {chats}",
        (255, 255, 255),
        font=arial,
    )
    draw.text(
        (600, 500),
        f"Version : 0.1.5",
        (255, 255, 255),
        font=arial,
    )
    draw.text(
        (600, 550),
        f"BoT : t.me\{username}",
        (255, 255, 255),
        font=arial,
    )
    try:
        os.remove(f"thumb{username}.png")
    except:
        pass
    background.save(f"{username}.png")
    return f"{username}.png"


######################


####################

OFFPV = []


@Client.on_message(
    filters.command(
        [
            "• چالاککردنی پەیوەندی •",
            "چالاککردنی پەیوەندی",
            "ناچالاککردنی پەیوەندی",
            "• ناچالاککردنی پەیوەندی •",
        ],
        "",
    )
)
async def byyye(client, message):
    user = message.from_user.username
    dev = await get_dev(client.me.username)
    if user in OWNER or message.from_user.id == dev:
        text = message.text
        if text == "چالاککردنی پەیوەندی" or text == "• چالاککردنی پەیوەندی •":
            if not client.me.username in OFFPV:
                await message.reply_text("**♪ فەرمانی پەیوەندی پێشتر چالاککراوە 💎.**")
            try:
                OFFPV.remove(client.me.username)
                await message.reply_text("**♪ فەرمانی پەیوەندی چالاککرا 💎.**")
                return
            except:
                pass
        if text == "ناچالاککردنی پەیوەندی" or text == "• ناچالاککردنی پەیوەندی •":
            if client.me.username in OFFPV:
                await message.reply_text(
                    "**♪ فەرمانی پەیوەندی پێشتر ناچالاککراوە 💎.**"
                )
            try:
                OFFPV.append(client.me.username)
                await message.reply_text("**♪ فەرمانی پەیوەندی ناچالاککرا 💎.**")
                return
            except:
                pass


# __________________________________


#########################
@Client.on_message(filters.private)
async def botoot(client: Client, message: Message):
    if not client.me.username in OFFPV:
        if await joinch(message):
            return
        bot_username = client.me.username
        user_id = message.chat.id
        if not await is_served_user(client, user_id):
            await add_served_user(client, user_id)
        dev = await get_dev(bot_username)
        if (
            message.from_user.id == dev
            or message.chat.username in OWNER
            or message.from_user.id == client.me.id
        ):
            if message.reply_to_message:
                u = message.reply_to_message.forward_from
                try:
                    await client.send_message(u.id, text=message.text)
                    await message.reply_text(
                        f"**♪ بە سەرکەوتوویی نامەکەت بۆ {u.mention} نێردرا 💎.**"
                    )
                except Exception:
                    pass
        else:
            try:
                await client.forward_messages(dev, message.chat.id, message.id)
                await client.forward_messages(OWNER[0], message.chat.id, message.id)
            except Exception as e:
                pass
    message.continue_propagation()


# ...............................


@Client.on_message(filters.new_chat_members)
async def welcome(client: Client, message):
    try:
        bot = client.me
        bot_username = bot.username
        if message.new_chat_members[0].username == "Hawaall":
            try:
                chat_id = message.chat.id
                user_id = message.new_chat_members[0].id
                await client.promote_chat_member(
                    chat_id,
                    user_id,
                    privileges=enums.ChatPrivileges(
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
                await client.set_administrator_title(chat_id, user_id, "𝐇𝐚𝐰𝐚𝐥𝐥🔥 ꨄᵉⁿᵈᨒ")
            except:
                pass
            return await message.reply_text(
                f"**♪ خاوەنی سەرچاوە جۆینی گرووپ بوو 💎.\n♪ بەخێربێی : @Hawaall 💎.**"
            )
        dev = await get_dev(bot_username)
        if message.new_chat_members[0].id == dev:
            try:
                await client.promote_chat_member(
                    message.chat.id,
                    message.new_chat_members[0].id,
                    privileges=enums.ChatPrivileges(
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
                await client.set_administrator_title(
                    message.chat.id, message.new_chat_members[0].id, "خاوەنی بۆت"
                )
            except:
                pass
            return await message.reply_text(
                f"**♪ خاوەنی بۆت جۆینی گرووپ بوو 💎.\n♪ بەخێربێی : {message.new_chat_members[0].mention} 💎.**"
            )
        if message.new_chat_members[0].id == bot.id:
            photo = bot.photo.big_file_id
            photo = await client.download_media(photo)
            chat_id = message.chat.id
            userbot = await get_userbot(bot_username)
            link = await client.export_chat_invite_link(message.chat.id)
            nn = await get_dev_name(client, bot_username)
            ch = await get_channel(bot_username)
            gr = await get_group(bot_username)
            button = [
                [
                    InlineKeyboardButton(text="♪. 𝑪𝒉𝒂𝒏𝒆𝒆𝒍", url=f"{ch}"),
                    InlineKeyboardButton(text="𝑮𝒓𝒐𝒖𝒑 ♪.", url=f"{gr}"),
                ],
                [InlineKeyboardButton(text=f"{nn}", user_id=f"{dev}")],
                [
                    InlineKeyboardButton(
                        text="زیادم بکە بۆ گرووپ یان کەناڵت ⚡",
                        url=f"https://t.me/{bot.username}?startgroup=True",
                    )
                ],
            ]
            Text = f"""**
♪ سوپاس بۆ زیادکردنم بۆ گرووپ 💎.
♪ گرووپ : {message.chat.title}
♪ بۆت بکە بە ئەدمین 💎.
♪ خودکارانە چالاك دەبێت 💎.
♪ ئێستا دەتوانم گۆرانی پەخش بکەم 💎.
**"""
            await message.reply_photo(
                photo=photo, caption=Text, reply_markup=InlineKeyboardMarkup(button)
            )
            logger = await get_dev(bot_username)
            await add_served_chat(client, chat_id)
            await user.join_chat(link)
            chats = len(await get_served_chats(client))
            return await client.send_photo(
                logger,
                photo=random.choice(joinandleft),
                caption=f"**● ꒐ بۆتی گۆرانی زیادکرا بۆ گرووپ 💎.\n● ꒐ ناوی گرووپ : [{message.chat.title}](https://t.me/{message.chat.username}) 💎.\n● ꒐ ئایدی گرووپ : {message.chat.id} 💎.\n● ꒐ لەلایەن : {message.from_user.mention} 💎.\n● ꒐ ژماری گرووپەکان : {chats} 💎.**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"نوێکارییەکانی بۆت 🍻", url=f"https://t.me/Haawall"
                            )
                        ]
                    ]
                ),
            )
    except:
        pass


@Client.on_message(filters.left_chat_member)
async def bot_kicked(client: Client, message):
    bot = client.me
    bot_username = bot.username
    if message.left_chat_member.id == bot.id:
        logger = await get_dev(bot_username)
        chat_id = message.chat.id
        await client.send_photo(
            logger,
            photo=random.choice(joinandleft),
            caption=f"**● ꒐ بۆت باندکرا 💎.**\n**● ꒐ ناوی گرووپ : {message.chat.title} 💎.**\n**● ꒐ ئایدی گرووپ : `{message.chat.id}` 💎.**\n**● ꒐ دەرکرا لەلایەن : {message.from_user.mention} 💎.**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"نوێکارییەکانی بۆت 🍻", url=f"https://t.me/Haawall"
                        )
                    ]
                ]
            ),
        )
        return await del_served_chat(client, chat_id)


@Client.on_message(
    filters.command(["/start", "• گەڕانەوە بۆ لیستی سەرەکی •"], "") & filters.private
)
async def start(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        if await joinch(message):
            return
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    nn = await get_dev_name(client, bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        kep = ReplyKeyboardMarkup(
            [
                ["• سەرچاوە •", "• بەشی چالاك و ناچالاك •"],
                ["• بەشی گۆڕین •", "• بەشی بۆت •"],
                ["• بەشی ئەکاونتی یاریدەدەر •", "• بەشی فۆروارد •"],
                ["• خاوەنی بۆت •", "• پڕۆگرامساز •"],
            ],
            resize_keyboard=True,
        )
        return await message.reply_text(
            "**◗⋮◖ بەخێربێی، گەشەپێدەری ئازیز 💎.**", reply_markup=kep, quote=True
        )
    else:
        kep = ReplyKeyboardMarkup(
            [
                ["خاوەنی بۆت", "گەشەپێدەری سەرچاوە"],
                ["سەرچاوە", "پینگ"],
                ["وێنە", "ستۆری"],
                ["وێنەی ئەنیمی", "فەرمانەکان"],
                ["گۆرانی", "زکر"],
                ["قورئانی پیرۆز", "ڤیدیۆی قورئان"],
                ["وێنەی کچان", "وێنەی خەمبار"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            "**◗⋮◖ بەخێربێیت، ئەندامی ئەزیز 💎.**", reply_markup=kep, quote=True
        )
        username = client.me.username
        if os.path.isfile(f"{username}.png"):
            photo = f"{username}.png"
        else:
            bot = await client.get_me()
            if not bot.photo:
                button = [
                    [
                        InlineKeyboardButton(
                            text="ᴇɴɢʟɪѕʜ 🇺🇲", callback_data=f"english"
                        ),
                        InlineKeyboardButton(
                            text="🧑🏻‍💻 کوردی", callback_data=f"kurdish"
                        ),
                    ],
                    [InlineKeyboardButton(text=f"{nn}", user_id=f"{dev}")],
                ]
                return await client.send_message(
                    message.chat.id,
                    "**● ꒐ تکایە کلیک لەسەر زمانەکە بکە\n● ꒐ کوردی یان ئینگلیزی\n\n● ꒐ 𝖯𝗅𝖾𝖺𝗌𝖾 𝖢𝗅𝗂𝖼𝗄 𝖮𝗇 𝖳𝗁𝖾 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾\n● ꒐ 𝖪𝗎𝗋𝖽𝗂𝗌𝗁 𝖮𝗋 𝖤𝗇𝗀𝗅𝗂𝗌𝗁**",
                    reply_to_message_id=message.id,
                    reply_markup=InlineKeyboardMarkup(button),
                )
            photo = bot.photo.big_file_id
            photo = await client.download_media(photo)
            username = client.me.username
            photo = await gen_bot(client, username, photo)
        button = [
            [
                InlineKeyboardButton(text="ᴇɴɢʟɪѕʜ 🇺🇲", callback_data=f"english"),
                InlineKeyboardButton(text="🧑🏻‍💻 کوردی", callback_data=f"kurdish"),
            ],
            [InlineKeyboardButton(text=f"{nn}", user_id=f"{dev}")],
        ]
        await client.send_photo(
            message.chat.id,
            photo=photo,
            caption="**● ꒐ تکایە کلیک لەسەر زمانەکە بکە\n● ꒐ کوردی یان ئینگلیزی\n\n● ꒐ 𝖯𝗅𝖾𝖺𝗌𝖾 𝖢𝗅𝗂𝖼𝗄 𝖮𝗇 𝖳𝗁𝖾 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾\n● ꒐ 𝖪𝗎𝗋𝖽𝗂𝗌𝗁 𝖮𝗋 𝖤𝗇𝗀𝗅𝗂𝗌𝗁**",
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup(button),
        )


############//((/start))//############
@Client.on_message(
    filters.command(["• بەشی چالاك و ناچالاك •", "بەشی چالاك و ناچالاك"], "")
)
async def helpercn(client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    userbot = await get_userbot(bot_username)
    me = userbot.me
    if message.chat.id == dev or message.chat.username in OWNER:
        kep = ReplyKeyboardMarkup(
            [
                ["• چالاککردنی پەیوەندی •", "• ناچالاککردنی پەیوەندی •"],
                ["• چالاککردنی گرووپی ئامار •", "• ناچالاککردنی گرووپی ئامار •"],
                ["• چالاککردنی جۆینی ناچاری •", "• ناچالاککردنی جۆینی ناچاری •"],
                ["• گەڕانەوە بۆ لیستی سەرەکی •"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            f"**◗⋮◖ بەخێربێی بۆ بەشی ⟨ چالاك و ناچالاك ⟩ 💎.**",
            reply_markup=kep,
            quote=True,
        )


@Client.on_message(
    filters.command(["بەشی گۆڕین", "• بەشی گۆڕین •"], "") & filters.private
)
async def cast(client: Client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    if message.chat.id == dev or message.chat.username in OWNER:
        kep = ReplyKeyboardMarkup(
            [
                ["• گۆڕینی ناوی بۆت •"],
                ["• گۆڕینی کەناڵی بۆت •", "• گۆڕینی گرووپی بۆت •"],
                ["• گۆڕینی گرووپی ئامار •"],
                ["• گۆڕینی کەناڵی سەرچاوە •", "• گۆڕینی گرووپی سەرچاوە •"],
                ["• گۆڕینی لۆگۆی سەرچاوە •"],
                ["• گەڕانەوە بۆ لیستی سەرەکی •"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            "**◗⋮◖ بەخێربێی بۆ بەشی ⟨ گۆڕین ⟩ 💎.**", reply_markup=kep
        )


@Client.on_message(filters.command(["بەشی بۆت", "• بەشی بۆت •"], ""))
async def Elasyoutyy(client, message):
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    chat = message.chat.id
    uesr = message.chat.username
    if chat == dev or uesr in OWNER:
        kep = ReplyKeyboardMarkup(
            [
                ["• ئامارەکان •", "• تێلی چالاك •"],
                ["• گرووپەکان •", "• بەکارهێنەرەکان •"],
                ["• گەڕانەوە بۆ لیستی سەرەکی •"],
            ],
            resize_keyboard=True,
        )
        await message.reply_text(
            f"**◗⋮◖ بەخێربێی بۆ بەشی ⟨ بۆت ⟩ 💎.**", reply_markup=kep, quote=True
        )


############//((/start))//############

bot = [
    "معاك يشق",
    "يسطا شغال شغال متقلقش",
    "بحبك يعم قول عايز اي",
    "يبني هتقول عايز اي ولا اسيبك وامشي ",
    "قلب {} من جوه",
    "نعم يقلب {} ",
    "قرفتني والله بس بحبك بقا اعمل اي",
    "خلاص هزرنا وضحكنا انطق بقا عايز اي ؟",
    "قوول يقلبو ",
    "طب بذمتك لو انت بوت ترضا حد يقرفقك كدا؟",
]

azkar = [
    "لا إِلَهَ إِلا أَنتَ سُبْحَانَكَ إِنِّي كُنتُ مِنَ الظَّالِمِينَ🌸",
    "اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ , وَشُكْرِكَ , وَحُسْنِ عِبَادَتِكَ🎈💞",
    "استغفر الله العظيم وأتوبُ إليه 🌹",
    "حَسْبِيَ اللَّهُ لا إِلَـهَ إِلاَّ هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيم"
    "ِ سبع مرات، كفاه الله تعالى ما أهمه من أمور الدنيا والآخرة🌹🌸",
    "ربنا اغفر لنا ذنوبنا وإسرافنا فِي أمرنا وثبت أقدامنا وانصرنا على القوم الكافرين🌸",
    "أشهد أنْ لا إله إلا الله وحده لا شريك له، وأشهد أن محمدًا عبده ورسوله🌺",
    "سبحان الله وبحمده سبحان الله العظيم🌸",
    "أشهد أنْ لا إله إلا الله وحده لا شريك له، وأشهد أن محمدًا عبده ورسوله🌺",
    "اللهم إنك عفو تُحب العفو فاعفُ عنّا 🌿🌹",
    "استغفر الله العظيم وأتوبُ إليه 🌹",
    "لا تقطع صلاتك، إن كنت قادراً على الصلاة في الوقت فصلِي و أكثر من الدعاء لتحقيق ما تتمنى💙",
    "قال ﷺ : ”حَيْثُمَا كُنْتُمْ فَصَلُّوا عَلَيَّ، فَإِنَّ صَلَاتَكُمْ تَبْلُغُنِي“.",
    "يا رب أفرحني بشيئاً انتظر حدوثه،اللهم إني متفائلاً بعطائك فاكتب لي ما أتمنى🌸",
    "﴿ رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي ﴾",
    "‏{ تَوَفَّنِي مُسْلِمًا وَأَلْحِقْنِي بِالصَّالِحِينَ }",
    "‏اللهّم لطفك بقلوبنا وأحوالنا وأيامنا ،‏اللهّم تولنا بسعتك وعظيم فضلك ",
    "ومن أحسن قولاً ممن دعا إلى الله وعمل صالحاً وقال أنني من المسلمين .💕",
    "‏إن الله لا يبتليك بشيء إلا وبه خيرٌ لك فقل الحمدلله.",
    "رَبِّ أَوْزِعْنِي أَنْ أَشْكُرَ نِعْمَتَكَ",
    "اللهم اشفي كل مريض يتألم ولا يعلم بحاله إلا أنت",
    "استغفر الله العظيم وأتوبُ إليه.",
    "‏لَم تعرف الدنيا عظيماً مِثله صلّوا عليه وسلموا تسليم",
    " أنتَ اللّطيف وأنا عبدُك الضّعيف اغفرلي وارحمني وتجاوز عنّي.",
    "ماتستغفر ربنا كده🥺❤️",
    "فاضي شويه نصلي ع النبي ونحز خته فى الجنه❤️❤️",
    "ماتوحدو ربنا يجماعه قولو لا اله الا الله❤️❤️",
    "يلا كل واحد يقول سبحان الله وبحمده سبحان الله العظيم 3 مرات🙄❤️",
    "قول لاحول ولا قوه الا بالله يمكن تفك كربتك🥺❤️",
    "اللهم صلي عللى سيدنا محمد ماتصلي على النبي كده",
    "- أسهل الطرق لإرضاء ربك، أرضي والديك 🥺💕",
    "- اللهُم صبراً ، اللهم جبراً ، اللهم قوّة",
    "أصبحنا وأصبح الملك لله ولا اله الا الله.",
    "‏إنَّ اللهَ يُحِبُ المُلحِينَ فِي الدُّعَاء.",
    "‏إن الله لا يخذل يداً رُفعت إليه أبداً.",
    "يارب دُعاء القلب انت تسمعه فأستجب لهُ.",
    "- اللهم القبول الذي لا يزول ❤️🍀.",
    "- اللهُم خذ بقلبّي حيث نورك الذي لا ينطفِئ.",
    "سبحان الله وبحمده ،سبحان الله العظيم.",
    "لا تعودوا أنفسكم على الصمت، اذكرو الله، استغفروه، سبّحوه، احمدوه،"
    " عودوا السنتكم على الذكر فإنها إن اعتادت لن تصمت أبدًا.",
    "- اللهم بلغنا رمضان وأجعلنا نختم القرآن واهدنا لبر الامان يالله يا رحمان 🌙",
    "بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العلي- ثلاث مرات -",
    "- اللهم احرمني لذة معصيتك وارزقني لذة طاعتك 🌿💜.",
    "- اللهُم إن في صوتي دُعاء وفي قلبِي أمنية اللهُم يسر لي الخير حيث كان.",
    "‏اللهم أرني عجائب قدرتك في تيسير أموري 💜.",
    "يغفر لمن يشاء إجعلني ممن تشاء يا الله.*",
    "‏يارب إن قصّرنا في عبادتك فاغفرلنا، وإن سهينا عنك بمفاتن الدنيا فردنا إليك رداً جميلاً 💜🍀",
    "صلوا على من قال في خطبة الوداع  ‏و إني مُباهٍ بكم الأمم يوم القيامة♥️⛅️",
    "اللهـم إجعلنا ممن تشهد أصابعهم بذكـر الشهادة قبل الموت 🌿💜.",
    "- وبك أصبحنا يا عظيم الشأن 🍃❤️.",
    "اللهُم الجنة ونعيَّم الجنة مع من نحب💫❤️🌹",
    "‏اللهم قلبًا سليمًا عفيفًا تقيًا نقيًا يخشاك سرًا وعلانية🤍🌱",
    "- أسجِد لربِك وأحضِن الارض فِي ذِ  لاضَاق صَدرِك مِن هَموم المعَاصِي 🌿.",
    "صلي على النبي بنيه الفرج❤️",
    "استغفر ربنا كده 3 مرات هتاخد ثواب كبير اوى❤️",
    "اشهد ان لا اله الا الله وان محمدا عبده ورسوله",
    "لا اله الا الله سيدنا محمد رسول الله🌿💜",
    "قول معايا - استغفر الله استفر الله استغفر الله -",
    "مُجرد ثانية تنفعِك : أستغفُرالله العظيِم وأتوب إليّه.",
    "أدعُ دُعاء الواثِق فالله لايُجرّبُ معه‌‏",
    "صلي على اشرف الخلق سيدنا محمد صلاةً الله عليه وسلم تسليما كثيرا ❤️",
    "ربي اجعلني مقيم الصلاة ومن ذريتي ربنا وتقبل دعاءنا . ربنا تقبل منا إنك أنت السميع العليم وتب علينا إنك أنت التواب الرحيم",
    "رب اغفر لي خطيئتي يوم الدين❤️",
    "اللهم اهدني فيمن هديت، وعافني فيمن عافيت، وتولني فيمن توليت، وبارك لي فيما أعطيت، وقني شرما قضيت، إنه لا يذل من واليت، تباركت ربنا وتعاليت",
    "اللهم إني أعوذ بك من عذاب النار، وأعوذ بك من عذاب القبر، وأعوذ بك من الفتن ما ظهر منها وما بطن، وأعوذ بك من فتنة الدجال",
    "اللهم إني أعوذ بك من علم لا ينفع وعمل لا يرفع وقلب لا يخشع وقول لا يسمع",
    "اللهم لا تخزني يوم القيامة",
    "اللهم إني أعوذ بك من صلاة لا تنفع",
    "اللهم إني أسألك الفردوس أعلى الجنة",
    "أَعـوذُ بِكَ مِنْ شَـرِّ ما صَنَـعْت، أَبـوءُ لَـكَ بِنِعْـمَتِـكَ عَلَـيَّ وَأَبـوءُ بِذَنْـبي فَاغْفـِرْ لي فَإِنَّـهُ لا يَغْـفِرُ الذُّنـوبَ إِلاّ أَنْتَ. مرة واحدة",
    "اللهم يا رحمن يا حنان يا منان استودعك يا رب قلبي فلا تجعل فيه أحدا سواك واستودعتك شهادة لا إله إلا الله فألهمني بها يا رب عند الممات واستودعك اللهم نفسي فلا تجعلني أخطو خطوة واحدة إلا في مرضاتك واستودعك روقي وعافيتي فاحفظها لي.",
    "اللهم يا كريم يا ودود يا رحيم يا عظيم انك قادر على كل شيء انك تقول للشيء كن فيكون ارحم اهلي رحمة دائمة واجعلهم من أهل الجنه في الفردوس لأعلي اللهم تقبلهم إليك واسعدهم بلقائك",
    "اللهم يا رحمن يارحيم ارحمني برحمتك الواسعه يارب ونقني من زنوبي مثل نقاء الثوب الأبيض من الدنس",
    "رَبَّنَا اغفِر لي وَلِوالِدَيَّ وَلِلمُؤمِنينَ يَومَ يَقومُ الحِسابُ",
    "رَّبِّ اغْفِرْ لِي وَلِوَالِدَيَّ وَلِمَن دَخَلَ بَيْتِيَ مُؤْمِنًا وَلِلْمُؤْمِنِينَ وَالْمُؤْمِنَاتِ وَلَا تَزِدِ الظَّالِمِينَ إِلَّا تَبَارًا",
    "اللهمَّ اغفر لوالدي وارحمهما كما ربّياني صغيراً، اللهمّ يا باسط اليدين بالعطايا ابسط على والدي من فضلك العظيم وجودك الواسع ما تشرح به صدرهما لعبادتك وطاعتك، والأنس بك والعمل بما يُرضيك، وبارك لهما في عُمرها، واغنهما من فضلك، وأعنهما في حلّهما وترحالهما وذهابهما وإيابهما، وأطل في عمرهما مع العافية في صحتهما ودِينهما، واجعل اللهمَّ آخر كلامهما من الدنيا لا إله إلّا الله محمدٌ رسول الله",
    "(اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالآخِرَةِ، اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ: فِي دِينِي وَدُنْيَايَ وَأَهْلِي، وَمَالِي، اللَّهُمَّ اسْتُرْ عَوْرَاتِي، وَآمِنْ رَوْعَاتِي، اللَّهُمَّ احْفَظْنِي مِنْ بَينِ يَدَيَّ، وَمِنْ خَلْفِي، وَعَنْ يَمِينِي، وَعَنْ شِمَالِي، وَمِنْ فَوْقِي، وَأَعُوذُ بِعَظَمَتِكَ أَنْ أُغْتَالَ مِنْ تَحْتِي)).",
    "يا حيّ يا قيّوم برحمتك أستغيث أصلح لي شأني كله ولا تكلني إلى نفسي طرفة عينٍ أبداً ...",
    "‏﴿ وَاذْكُر ربّكَ إِذَا نَسِيتَ ﴾ ",
    "- اللهم صلِ وسلم على نبينآ محمد ❥⇣",
    "((اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبَيِّنَا مُحَمَّدٍ)) (عشرَ مرَّاتٍ).",
    "اللهم يا عزيز يا جبار اجعل قلوبنا تخشع من تقواك واجعل عيوننا تدمع من خشياك واجعلنا يا رب من أهل التقوى وأهل المغفر",
    "استغفر الله و اتوب اليه - استغفر الله و اتوب اليه - استغفر الله و اتوب اليه - استغفر الله و اتوب اليه - استغفر الله و اتوب الي",
    "اللهم إنك عفو تُحب العفو فاعفُ عن",
    "اللهم إني أسألك الثبات في الامر والعزيمة على الرشد واسالك قلبا سليما ولسانا صادقا واسالك شكر نعمتك و حسن عبادت",
    "اللهم إني أسألك العافية في الدنيا والآخرة، اللهم إني أسألك العفو والعافية في ديني ودنياي، وأهلي ومالي، اللهم استُر عوراتي، وآمِن رَوعاتي، اللهم احفظني من بين يدي ومن خلفي، وعن يميني وعن شمالي، ومن فوقي، وأعوذ بعظمتك أن أُغتال من تحتي",
    "((اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ)).",
    "((لاَ إِلَهَ إِلاَّ اللَّهُ، وَحْدَهُ لاَ شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ)) (مائةَ مرَّةٍ).",
    "((اللَّهُمَّ عَالِمَ الغَيْبِ وَالشَّهَادَةِ فَاطِرَ السَّمَوَاتِ وَالْأَرْضِ، رَبَّ كُلِّ شَيْءٍ وَمَلِيكَهُ، أَشْهَدُ أَنْ لاَ إِلَهَ إِلاَّ أَنْتَ، أَعُوذُ بِكَ مِنْ شَرِّ نَفْسِي، وَمِنْ شَرِّ الشَّيْطانِ وَشِرْكِهِ، وَأَنْ أَقْتَرِفَ عَلَى نَفْسِي سُوءاً، أَوْ أَجُرَّهُ إِلَى مُسْلِمٍ))",
    "اللهم اكفني بحلالك عن حرامك، وأغنني بفضلك عمن سواك",
    "(بِسْمِ اللَّهِ، تَوَكَّلْتُ عَلَى اللَّهِ، وَلَاَ حَوْلَ وَلَا قُوَّةَ إِلاَّ بِاللَّهِ)",
    "((أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ)) (مِائَةَ مَرَّةٍ فِي الْيَوْمِ).",
    "اللهم نشكوا إليك ضعفنا وقلة حيلتنا من امرنا فأغثنا وارحمنا واغفرلنا ولا تكل امرنا لمن لايخافك ولا يرحمنا ولا تؤخذنا بما فعل السفهاء منا",
    "مَنْ كَانَ آخِرُ كَلاَمِهِ لاَ إِلَهَ إِلاَّ اللَّهُ دَخَلَ الْجَنَّة"
    "االلَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ , وَشُكْرِكَ , وَحُسْنِ عِبَادَتِكَ🎈💞 ",
    "من الأدعية النبوية المأثورة:اللهمَّ زَيِّنا بزينة الإيمان",
    "اااللهم يا من رويت الأرض مطرا أمطر قلوبنا فرحا 🍂 ",
    "اا‏اللَّهُـمَّ لَڪَ الحَمْـدُ مِنْ قَـا؏ِ الفُـؤَادِ إلىٰ ؏َـرشِڪَ المُقـدَّس حَمْـدَاً يُوَافِي نِـ؏ـمَڪ 💙🌸",
    "﴿وَاذْكُرِ اسْمَ رَبِّكَ وَتَبَتَّلْ إِلَيْهِ تَبْتِيلًا﴾🌿✨",
    "﴿وَمَن يَتَّقِ اللهَ يُكَفِّرْ عَنْهُ سَيِّئَاتِهِ وَيُعْظِمْ لَهُ أَجْرًا﴾",
    "«سُبْحَانَ اللهِ ، وَالحَمْدُ للهِ ، وَلَا إلَهَ إلَّا اللهُ ، وَاللهُ أكْبَرُ ، وَلَا حَوْلَ وَلَا قُوَّةَ إلَّا بِاللهِ»🍃",
    "وذُنُوبًا شوَّهتْ طُهْرَ قُلوبِنا؛ اغفِرها يا ربّ واعفُ عنَّا ❤️",
    "«اللَّهُمَّ اتِ نُفُوسَنَا تَقْوَاهَا ، وَزَكِّهَا أنْتَ خَيْرُ مَنْ زَكَّاهَا ، أنْتَ وَلِيُّهَا وَمَوْلَاهَا»🌹",
    "۝‏﷽إن اللَّه وملائكته يُصلُّون على النبي ياأيُّها الذين امنوا صلُّوا عليه وسلِّموا تسليما۝",
    "فُسِبًحً بًحًمًدٍ ربًکْ وٌکْنِ مًنِ الَسِاجّدٍيَنِ 🌿✨",
    "اأقُمً الَصّلَاةّ لَدٍلَوٌکْ الَشُمًسِ إلَيَ غُسِقُ الَلَيَلَ🥀🌺",
    "نِسِتٌغُفُرکْ ربًيَ حًيَتٌ تٌلَهّيَنِا الَدٍنِيَا عٌنِ ذِکْرکْ🥺😢",
    "وٌمًنِ أعٌرض عٌنِ ذِکْريَ فُإنِ لَهّ مًعٌيَشُةّ ضنِکْا 😢",
    "وٌقُرأنِ الَفُجّر إنِ قُرانِ الَفُجّر کْانِ مًشُهّوٌدٍا🎀🌲",
    "اأّذّأّ أّلَدِنِيِّأّ نَِّستّګوِ أّصٌلَګوِ زِّوِروِ أّلَمَقِأّبِر💔",
    "حًتٌيَ لَوٌ لَمًتٌتٌقُنِ الَخِفُظُ فُمًصّاحًبًتٌ لَلَقُرانِ تٌجّعٌلَکْ مًنِ اهّلَ الَلَهّ وٌخِاصّتٌهّ❤🌱",
    "وٌإذِا رضيَتٌ وٌصّبًرتٌ فُهّوٌ إرتٌقُاء وٌنِعٌمًةّ✨??",
    "«ربً اجّعٌلَنِيَ مًقُيَمً الَصّلَاةّ وٌمًنِ ذِريَتٌيَ ربًنِا وٌتٌقُبًلَ دٍعٌاء 🤲",
    "ااعٌلَمً انِ رحًلَةّ صّبًرکْ لَهّا نِهّايَهّ عٌظُيَمًهّ مًحًمًلَهّ بًجّوٌائزٍ ربًانِيَهّ مًدٍهّشُهّ🌚☺️",
    "اإيَاکْ وٌدٍعٌوٌةّ الَمًظُلَوٌمً فُ إنِهّا تٌصّعٌدٍ الَيَ الَلَهّ کْأنِهّا شُرارهّ مًنِ نِار 🔥🥺",
    "االَلَهّمً انِقُذِ صّدٍوٌرنِا مًنِ هّيَمًنِهّ الَقُلَقُ وٌصّبً عٌلَيَهّا فُيَضا مًنِ الَطِمًأنِيَنِهّ✨🌺",
    "يَابًنِيَ إنِ صّلَاح الَحًيَاةّ فُ أتٌجّاهّ الَقُبًلَهّ 🥀🌿",
    "الَلَهّمً ردٍنِا إلَيَکْ ردٍا جّمًيَلَا💔🥺",
]


@Client.on_message(filters.command(["/alive", "/source", "سەرچاوە", "• سەرچاوە •"], ""))
async def alive(client: Client, message):
    chat_id = message.chat.id
    bot = client.me
    bot_username = client.me.username
    ch = await get_channelsr(client.me.username)
    gr = await get_groupsr(client.me.username)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝗚𝗿𝗼𝘂𝗽 🖱️", url=f"{gr}"),
                InlineKeyboardButton("𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🖱️", url=f"{ch}"),
            ],
            [InlineKeyboardButton(f"{OWNER_NAME}", url=f"https://t.me/{OWNER[0]}")],
            [
                InlineKeyboardButton(
                    "˹ᴍ ᴀ ᴋ ᴇ ꝛ ✗ ʜ ᴀ ᴡ ᴀ ʟ˼", url=f"https://t.me/creatmusicbot"
                ),
            ],
            [
                InlineKeyboardButton(
                    "زیادم بکە بۆ گرووپت ❤️",
                    url="https://t.me/{bot_username}?startgroup=true",
                )
            ],
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


@app.on_message(filters.command(["/help", "فەرمان", "فەرمانەکان"], ""))
async def starhelp(client: Client, message: Message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        if await joinch(message):
            return
    chat_id = message.chat.id
    bot_username = client.me.username
    bot = client.me
    dev = await get_dev(bot.username)
    devname = await get_dev_name(client, bot.username)
    photo = bot.photo.big_file_id
    photo = await client.download_media(photo)
    await message.reply_photo(
        photo=photo,
        caption=f"**● ꒐ تکایە کلیک لەسەر زمانەکە بکە\n● ꒐ کوردی یان ئینگلیزی\n\n● ꒐ 𝖯𝗅𝖾𝖺𝗌𝖾 𝖢𝗅𝗂𝖼𝗄 𝖮𝗇 𝖳𝗁𝖾 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾\n● ꒐ 𝖪𝗎𝗋𝖽𝗂𝗌𝗁 𝖮𝗋 𝖤𝗇𝗀𝗅𝗂𝗌𝗁**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🧑🏻‍💻 کوردی", callback_data=f"kurdish")],
                [InlineKeyboardButton("ᴇɴɢʟɪѕʜ 🇺🇲", callback_data=f"english")],
                [InlineKeyboardButton(f"{devname}", user_id=f"{dev}")],
                [
                    InlineKeyboardButton(
                        "زیادم بکە بۆ گرووپت ❤️",
                        url="https://t.me/{bot_username}?startgroup=true",
                    )
                ],
            ]
        ),
    )
    try:
        os.remove(photo)
    except:
        pass


@Client.on_message(filters.command(["ping", "پینگ"], ""))
async def ping_pong(client: Client, message: Message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        if await joinch(message):
            return
    start = time()
    m_reply = await message.reply_text("**کەمێ بۆستە**")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(filters.command(["چالاککردن", "چالاکردن"], "") & ~filters.private)
async def pipong(client: Client, message: Message):
    if len(message.command) == 1:
        if not message.chat.type == enums.ChatType.PRIVATE:
            if await joinch(message):
                return
        await message.reply_text("**بە سەرکەوتوویی بۆت چالاککرا ✅**")
        return


@Client.on_message(filters.command(["• پڕۆگرامساز •", "پڕۆگرامساز"], ""))
async def deev(client: Client, message: Message):
    if await joinch(message):
        return
    user = await client.get_chat(chat_id="833360381")
    name = user.first_name
    username = user.username
    bio = user.bio
    user_id = user.id
    photo = user.photo.big_file_id
    photo = await client.download_media(photo)
    link = f"https://t.me/{message.chat.username}"
    title = message.chat.title if message.chat.title else message.chat.first_name
    chat_title = (
        f"**بەکارهێنەر : {message.from_user.mention} \nگرووپ : {title}**"
        if message.from_user
        else f"**گرووپ : {message.chat.title}**"
    )
    try:
        await client.send_message(
            username,
            f"**کەسێک هەیە پێویستی بە تۆیە، گەشەپێدەری سەرەکی بەڕێز**\n{chat_title}\nئایدی گرووپ : `{message.chat.id}`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"{title}", url=f"{link}")]]
            ),
        )
    except:
        pass
    await message.reply_photo(
        photo=photo,
        caption=f"**● ꒐ ناوی : {name}** \n**● ꒐ یوزەری : @{username}**\n**● ꒐ بایۆی : {bio}**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]
        ),
    )
    try:
        os.remove(photo)
    except:
        pass


@Client.on_message(filters.command(["گەشەپێدەر", "• خاوەنی بۆت •", "خاوەنی بۆت"], ""))
async def dev(client: Client, message: Message):
    if await joinch(message):
        return
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    user = await client.get_chat(chat_id=dev)
    name = user.first_name
    username = user.username
    bio = user.bio
    user_id = user.id
    photo = user.photo.big_file_id
    photo = await client.download_media(photo)
    link = f"https://t.me/{message.chat.username}"
    title = message.chat.title if message.chat.title else message.chat.first_name
    chat_title = (
        f"**بەکارهێنەر : {message.from_user.mention} \nگرووپ : {title}**"
        if message.from_user
        else f"**گرووپ : {message.chat.title}**"
    )
    try:
        await client.send_message(
            username,
            f"**کەسێک هەیە پێویستی بە تۆیە، گەشەپێدەری سەرەکی بەڕێز**\n{chat_title}\nئایدی گرووپ : `{message.chat.id}`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"{title}", url=f"{link}")]]
            ),
        )
    except:
        pass
    await message.reply_photo(
        photo=photo,
        caption=f"**● ꒐ ناوی : {name}** \n**● ꒐ یوزەری : @{username}**\n**● ꒐ بایۆی : {bio}**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]
        ),
    )
    try:
        os.remove(photo)
    except:
        pass


@Client.on_message(filters.command(["گەشەپێدەری سەرچاوە"], ""))
async def debsu(client: Client, message: Message):
    if await joinch(message):
        return
    bot_username = client.me.username
    dev = await get_dev(bot_username)
    user = await client.get_chat(chat_id=DEV_USER)
    name = user.first_name
    username = user.username
    bio = user.bio
    user_id = user.id
    photo = user.photo.big_file_id
    photo = await client.download_media(photo)
    link = f"https://t.me/{message.chat.username}"
    title = message.chat.title if message.chat.title else message.chat.first_name
    chat_title = (
        f"**بەکارهێنەر : {message.from_user.mention} \nگرووپ : {title}**"
        if message.from_user
        else f"**گرووپ : {message.chat.title}**"
    )
    try:
        await client.send_message(
            username,
            f"**کەسێک هەیە پێویستی بە تۆیە، گەشەپێدەری سەرەکی بەڕێز\n{chat_title}\nئایدی گرووپ : {message.chat.id}**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(f"{title}", url=f"{link}")]]
            ),
        )
    except:
        pass
    await message.reply_photo(
        photo=photo,
        caption=f"**● ꒐ ناوی : {name}** \n**● ꒐ یوزەری : @{username}**\n**● ꒐ بایۆی : {bio}**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]
        ),
    )
    try:
        os.remove(photo)
    except:
        pass


@Client.on_message(filters.command(["• گۆڕینی ناوی بۆت •", "گۆڕینی ناوی بۆت"], ""))
async def set_bot(client: Client, message):
    NAME = await client.ask(
        message.chat.id,
        "**◗⋮◖ ئێستا ناوە نوێیەکە بنێرە 💎.**",
        filters=filters.text,
        timeout=30,
    )
    BOT_NAME = NAME.text
    bot_username = client.me.username
    await set_bot_name(bot_username, BOT_NAME)
    await message.reply_text("**◗⋮◖ بە سەرکەوتوویی ناوی بۆت گۆڕا 💎.**")


@Client.on_message(
    filters.command(["• گۆڕینی لۆگۆی سەرچاوە •", "گۆڕینی لۆگۆی سەرچاوە"], "")
)
async def set_vi_so(client: Client, message):
    if message.chat.username in OWNER:
        NAME = await client.ask(
            message.chat.id,
            "**◗⋮◖ لینکی لۆگۆی سەرچاوە بنێرە 💎.\n♪ نموونە ⟨ https://telegra.ph/file/5052303e233d674acebd1.jpg ⟩ 💎.**",
            filters=filters.text,
            timeout=30,
        )
    if not message.chat.username in OWNER:
        await message.reply_text("**تەنیا خاوەنی سەرچاوە داتوانێت -🖱️**")
        VID_SO = NAME.text
        bot_username = client.me.username
        await set_video_source(bot_username, VID_SO)
        await message.reply_text("**♪ بە سەرکەوتوویی لۆگۆی سەرچاوە گۆڕا 💎.**")


@Client.on_message(
    filters.command(["• گۆڕینی گەشەپێدەری سەرچاوە •", "گۆڕینی گەشەپێدەری سەرچاوە"], "")
)
async def set_dev_username(client: Client, message):
    if message.chat.username in OWNER:
        NAME = await client.ask(
            message.chat.id,
            "**◗⋮◖ یوزەری گەشەپێدەری نوێ بنێرە 💎.**",
            filters=filters.text,
            timeout=300,
        )
    if not message.chat.username in OWNER:
        await message.reply_text("**تەنیا خاوەنی سەرچاوە داتوانێت -🖱️**")
        CH_DEV_USER = NAME.text
        bot_username = client.me.username
        await set_dev_user(bot_username, CH_DEV_USER)
        await message.reply_text("**♪ بە سەرکەوتوویی گەشەپێدەری سەرچاوە گۆڕا 💎.**")


@Client.on_message(filters.text)
async def bott(client: Client, message: Message):
    bot_username = client.me.username
    BOT_NAME = await get_bot_name(bot_username)
    if message.text == BOT_NAME:
        bar = random.choice(bot).format(BOT_NAME)
        await message.reply_text(
            f"**[{bar}](https://t.me/{bot_username}?startgroup=True)**",
            disable_web_page_preview=True,
        )
    message.continue_propagation()


@Client.on_message(~filters.private)
async def booot(client: Client, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(client, chat_id):
        try:
            await add_served_chat(client, chat_id)
            chats = len(await get_served_chats(client))
            bot_username = client.me.username
            dev = await get_dev(bot_username)
            username = (
                f"https://t.me/{message.chat.username}"
                if message.chat.username
                else None
            )
            mention = (
                message.from_user.mention if message.from_user else message.chat.title
            )
            await client.send_message(
                dev,
                f"**گرووپی نوێ چالاککرا {chats} گرووپ**\nNew Group : [{message.chat.title}]({username})\nId : {message.chat.id} \nBy : {mention}",
                disable_web_page_preview=True,
            )
            await client.send_message(
                chat_id, f"**◗⋮◖ بە سەرکەوتوویی بۆت چالاککرا 💎.**"
            )
            return
        except:
            pass
    message.continue_propagation()


@Client.on_message(filters.command(["زکری بەیانیان", "زکر"], ""))
async def axkary(client: Client, message: Message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        if await joinch(message):
            return
    bar = random.choice(azkar)
    await message.reply_text(f"**{bar}**", disable_web_page_preview=True)


@Client.on_message(filters.command(["لینک"], ""))
async def llink(client: Client, message: Message):
    if not message.from_user.username in ["Hawaall"]:
        return
    chat_id = message.text.split(None, 1)[1].strip()
    invitelink = await client.export_chat_invite_link(chat_id)
    await message.reply_text(
        "**♪ لینکی گرووپ  💎.**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("لینک", url=f"{invitelink}")]]
        ),
    )


lisetanme = []


@Client.on_message(filters.command(["anime", "وێنەی ئەنیمی", "ئەنیمی"], ""))
async def sssora(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(lisetanme) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("LoreBots7"):
            if msg.media:
                lisetanme.append(msg)
    phot = random.choice(lisetanme)
    photo = f"https://t.me/LoreBots7/{phot.id}"
    await message.reply_photo(
        photo=photo,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


lisethazen = []


@Client.on_message(filters.command(["وێنەی خەمبار", "sad"], ""))
async def soorr4(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(lisethazen) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("PVVVV"):
            if msg.media:
                lisethazen.append(msg)
    phot = random.choice(lisethazen)
    photo = f"https://t.me/PVVVV/{phot.id}"
    await message.reply_photo(
        photo=photo,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


lisetbnat = []


@Client.on_message(filters.command(["وێنەی کچان", "کچان"], ""))
async def soora4(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(lisetbnat) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("ZSZZW"):
            if msg.media:
                lisetbnat.append(msg)
    phot = random.choice(lisetbnat)
    photo = f"https://t.me/ZSZZW/{phot.id}"
    await message.reply_photo(
        photo=photo,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


listsoer = []


@Client.on_message(filters.command(["وێنە", "وینە", "ڕەسم", "رەسم"], ""))
async def sssor(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(listsoer) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("Picture_elnqyb"):
            if msg.media:
                listsoer.append(msg)
    phot = random.choice(listsoer)
    photo = f"https://t.me/Picture_elnqyb/{phot.id}"
    await message.reply_photo(
        photo=photo,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


listmu = []


@Client.on_message(filters.command(["گ", "گۆرانی"], ""))
async def voece(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(listmu) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("ZWZZ7"):
            if msg.media:
                listmu.append(msg.id)
    audi = random.choice(listmu)
    audio = f"https://t.me/ZWZZ7/{audi}"
    await message.reply_audio(
        audio=audio,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


listvid = []


@Client.on_message(filters.command(["ستۆری", "ستوری"], ""))
async def videoo(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(listvid) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("videi_semo"):
            if msg.video:
                listvid.append(msg.id)
    id = random.choice(listvid)
    video = f"https://t.me/videi_semo/{id}"
    await message.reply_video(
        video=video,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


listvide = []


@Client.on_message(filters.command(["v", "ڤیدیۆ"], ""))
async def videooo(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(listvide) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("IQVIDE"):
            if msg.video:
                listvide.append(msg.id)
    id = random.choice(listvid)
    video = f"https://t.me/IQVIDE/{id}"
    await message.reply_video(
        video=video,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


listvidquran = []


@Client.on_message(filters.command(["ڤیدیۆی قورئان", "ستوري قران", "ڤ قورئان"], ""))
async def qurann(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(listvidquran) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("a9li91"):
            if msg.video:
                listvidquran.append(msg.id)
    id = random.choice(listvidquran)
    video = f"https://t.me/a9li91/{id}"
    await message.reply_video(
        video=video,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


listmuqurannn = []


@Client.on_message(
    filters.command(["ق", "قران", "قران كريم", "قورئان", "قورئانی پیرۆز"], "")
)
async def qurann2(client, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        await joinch(message)
    if len(listmuqurannn) == 0:
        user = await get_userbot(client.me.username)
        async for msg in user.get_chat_history("alkoraan4000"):
            if msg.media:
                listmuqurannn.append(msg.id)
    audi = random.choice(listmuqurannn)
    audio = f"https://t.me/alkoraan4000/{audi}"
    await message.reply_audio(
        audio=audio,
        caption="**♪ 𝑱𝒐𝒊𝒏 ➧ @Haawall 💎.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}",
                    )
                ],
            ]
        ),
    )


@Client.on_message(filters.command(["ڕۆڵم", "رۆلم", "ڕۆلم"], ""))
async def bt(client: Client, message: Message):
    try:
        if not message.chat.type == enums.ChatType.PRIVATE:
            if await joinch(message):
                return
        userr = message.from_user
        bot_username = client.me.username
        dev = await get_dev(bot_username)
        if userr.username in OWNER:
            await message.reply_text("**♪ ڕۆڵت : گەشەپێدەر سەرچاوە 💎.**")
            return
        if userr.username in ["IQ7amo"]:
            await message.reply_text("**♪ ڕۆڵت : پڕۆگرامساز 💎.**")
            return
        if userr.id == dev:
            return await message.reply_text("**♪ ڕۆڵت : خاوەنی بۆت 💎.**")
        user = await message._client.get_chat_member(
            message.chat.id, message.from_user.id
        )
        if user.status == enums.ChatMemberStatus.OWNER:
            await message.reply_text("**♪ ڕۆڵت : خاوەنی گرووپ 💎.**")
            return
        if user.status == enums.ChatMemberStatus.ADMINISTRATOR:
            await message.reply_text("**♪ ڕۆڵت : ئەدمین 💎.**")
            return
        else:
            await message.reply_text("**♪ ڕۆڵت : ئەندام 💎.**")
    except:
        pass


iddof = []


@Client.on_message(filters.command(["داخستنی ئایدی"], "") & filters.group)
async def iddlock(client: Client, message):
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        if message.chat.id in iddof:
            return await message.reply_text("**♪ فەرمانی ئایدی پێشتر داخراوە 💎.**")
        iddof.append(message.chat.id)
        return await message.reply_text(
            "**♪ بە سەرکەوتوویی فەرمانی ئایدی داخسترا 💎.**"
        )
    else:
        return await message.reply_text(
            "**♪ ببورە ئەزیزم ئەم فەرمانە بۆ ئەدمینەکانە 💎.**"
        )


@Client.on_message(filters.command(["کردنەوەی ئایدی"], "") & filters.group)
async def iddopen(client: Client, message):
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        if not message.chat.id in iddof:
            return await message.reply_text("**♪ فەرمانی ئایدی پێشتر کراوەتەوە 💎.**")
        iddof.remove(message.chat.id)
        return await message.reply_text(
            "**♪ بە سەرکەوتوویی فەرمانی ئایدی کرایەوە 💎.**"
        )
    else:
        return await message.reply_text(
            "**♪ ببورە ئەزیزم ئەم فەرمانە بۆ ئەدمینەکانە 💎.**"
        )


@Client.on_message(filters.command(["ئایدی", "id", "ا"], ""))
async def muid(client: Client, message):
    if message.chat.id in iddof:
        return await message.reply_text(
            "**♪ فەرمانی ئایدی داخراوە لەلایەن ئەدمینەکان 💎.**"
        )
    user = await client.get_chat(message.from_user.id)
    chat_id = message.chat.id
    user_id = user.id
    username = user.username
    mentoin = user.mentoin
    bioo = user.bio
    photo = user.photo.big_file_id
    photo = await client.download_media(photo)
    if not id.get(message.from_user.id):
        id[user.id] = []
    idd = len(id[user.id])
    await message.reply_photo(
        photo=photo,
        caption=f"**● ꒐ نـاوت : {mentoin}\n● ꒐ ئـایدی : `{user_id}`\n● ꒐ یـوزەرت : [@{username}]\n● ꒐ بـایـۆ : {bioo}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{idd} 🤍", callback_data=f"heart{user_id}")],
            ]
        ),
    )


id = {}


@app.on_callback_query(filters.regex("heart"))
async def heart(client, query: CallbackQuery):
    callback_data = query.data.strip()
    callback_request = callback_data.replace("heart", "")
    username = int(callback_request)
    usr = await client.get_chat(username)
    if not query.from_user.mention in id[usr.id]:
        id[usr.id].append(query.from_user.mention)
    else:
        id[usr.id].remove(query.from_user.mention)
    idd = len(id[usr.id])
    await query.edit_message_text(
        f"**name : {usr.first_name}\nid : {usr.id}\nuser : [@{usr.username}]\nbio : {usr.bio}**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"{idd} 🤍", callback_data=f"heart{usr.id}")]]
        ),
    )
