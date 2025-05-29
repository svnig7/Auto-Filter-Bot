import random
import asyncio
import re, time
import math
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from datetime import datetime, timedelta
from info import STICKERS_IDS, ADMINS, URL, MAX_BTN, BIN_CHANNEL, IS_STREAM, DELETE_TIME, FILMS_LINK, AUTH_CHANNEL, IS_VERIFY, VERIFY_EXPIRE, LOG_CHANNEL, SUPPORT_GROUP, SUPPORT_LINK, UPDATES_LINK, PICS, PROTECT_CONTENT, IMDB, AUTO_FILTER, SPELL_CHECK, IMDB_TEMPLATE, AUTO_DELETE, LANGUAGES, IS_FSUB, PAYMENT_QR, GROUP_FSUB, PM_SEARCH, UPI_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid, ChatAdminRequired
from utils import get_size, is_subscribed, is_check_admin, get_wish, get_shortlink, get_verify_status, update_verify_status, get_readable_time, get_poster, temp, get_settings, save_group_settings , imdb
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results,delete_files
from fuzzywuzzy import process

BUTTONS = {}
CAP = {}
REACTIONS = ["", "", "", ""]

@Client.on_callback_query(filters.regex(r"^stream"))
async def aks_downloader(bot, query):
    file_id = query.data.split('#', 1)[1]
    msg = await bot.send_cached_media(chat_id=BIN_CHANNEL, file_id=file_id)
    watch = f"{URL}watch/{msg.id}"
    download = f"{URL}download/{msg.id}"
    btn= [[
        InlineKeyboardButton("ᴡᴀᴛᴄʜ", url=watch),
        InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ", url=download)
    ],[
        InlineKeyboardButton('❌ ᴄʟᴏsᴇ ❌', callback_data='close_data')
    ]]
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(btn)
    )
    
@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    #await message.react(emoji=random.choice(REACTIONS))
    settings = await get_settings(message.chat.id)
    chatid = message.chat.id
    userid = message.from_user.id if message.from_user else None
    if GROUP_FSUB:
        btn = await is_subscribed(client, message, settings['fsub']) if settings.get('is_fsub', IS_FSUB) else None
        if btn:
            btn.append(
                [InlineKeyboardButton("ᴜɴᴍᴜᴛᴇ ᴍᴇ 🔕", callback_data=f"unmuteme#{chatid}")]
            )
            reply_markup = InlineKeyboardMarkup(btn)
            try:
                await client.restrict_chat_member(chatid, message.from_user.id, ChatPermissions(can_send_messages=False))
                await message.reply_photo(
                    photo=random.choice(PICS),
                    caption=f"👋 ʜᴇʟʟᴏ {message.from_user.mention},\n\nᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ. 😇",
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
                return
            except Exception as e:
                print(e)
    else:
        pass
    if settings["auto_filter"]:
        if not userid:
            await message.reply("ɪ'ᴍ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ ғᴏʀ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ !")
            return

        # REMOVE the group ID check and allow full result
        await auto_filter(client, message)
            
        if message.text.startswith("/"):
            return
            
        elif '@admin' in message.text.lower() or '@admins' in message.text.lower():
            if await is_check_admin(client, message.chat.id, message.from_user.id):
                return
            admins = []
            async for member in client.get_chat_members(chat_id=message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                if not member.user.is_bot:
                    admins.append(member.user.id)
                    if member.status == enums.ChatMemberStatus.OWNER:
                        if message.reply_to_message:
                            try:
                                sent_msg = await message.reply_to_message.forward(member.user.id)
                                await sent_msg.reply_text(f"#ᴀᴛᴛᴇɴᴛɪᴏɴ\n★ ᴜsᴇʀ : {message.from_user.mention}\n★ ɢʀᴏᴜᴘ : {message.chat.title}\n\n★ <a href={message.reply_to_message.link}>ɢᴏ ᴛᴏ ᴍᴇssᴀɢᴇ</a>", disable_web_page_preview=True)
                            except:
                                pass
                        else:
                            try:
                                sent_msg = await message.forward(member.user.id)
                                await sent_msg.reply_text(f"#ᴀᴛᴛᴇɴᴛɪᴏɴ\n★ ᴜsᴇʀ : {message.from_user.mention}\n★ ɢʀᴏᴜᴘ : {message.chat.title}\n\n★ <a href={message.link}>ɢᴏ ᴛᴏ ᴍᴇssᴀɢᴇ</a>", disable_web_page_preview=True)
                            except:
                                pass
            hidden_mentions = (f'[\u2064](tg://user?id={user_id})' for user_id in admins)
            await message.reply_text('ʀᴇᴘᴏʀᴛ sᴇɴᴛ !' + ''.join(hidden_mentions))
            return

        elif re.findall(r'https?://\S+|www\.\S+|t\.me/\S+', message.text):
            if await is_check_admin(client, message.chat.id, message.from_user.id):
                return
            await message.delete()
            return await message.reply('ʟɪɴᴋs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ʜᴇʀᴇ !')
        
        elif '#request' in message.text.lower():
            if message.from_user.id in ADMINS:
                return
            await client.send_message(LOG_CHANNEL, f"#ʀᴇᴏ̨ᴜᴇsᴛ\n★ ᴜsᴇʀ : {message.from_user.mention}\n★ ɢʀᴏᴜᴘ : {message.chat.title}\n\n★ ᴍᴇssᴀɢᴇ : {re.sub(r'#request', '', message.text.lower())}")
            await message.reply_text("ʀᴇᴏ̨ᴜᴇsᴛ sᴇɴᴛ !")
            return
            
        else:
            await auto_filter(client, message)
    else:
        k = await message.reply_text('ᴀᴜᴛᴏ ғɪʟᴛᴇʀ ᴏғғ ! ❌')
        await asyncio.sleep(5)
        await k.delete()
        try:
            await message.delete()
        except:
            pass

@Client.on_message(filters.private & filters.text)
async def pm_search(client, message):
    if PM_SEARCH:
        await auto_filter(client, message)
    else:
        files, n_offset, total = await get_search_results(message.text)
        if int(total) != 0:
            btn = [[
                InlineKeyboardButton("ʜᴇʀᴇ", url=FILMS_LINK)
            ]]
            await message.reply_text(f'ᴛᴏᴛᴀʟ {total} ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ', reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴅᴏɴ'ᴛ ᴄʟɪᴄᴋ ᴏᴛʜᴇʀs ʀᴇsᴜʟᴛs !", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nsᴇɴᴅ ɴᴇᴡ ʀᴇᴏ̨ᴜᴇsᴛ ᴀɢᴀɪɴ !", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    temp.FILES[key] = files
    settings = await get_settings(query.message.chat.id)
    del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    files_link = ''

    if settings['links']:
        btn = []
        for file_num, file in enumerate(files, start=offset+1):
            files_link += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {file.file_name}</a></b>"""
    else:
        btn = [[
            InlineKeyboardButton(text=f"📂 {get_size(file.file_size)} {file.file_name}", callback_data=f'file#{file.file_id}')
        ]
            for file in files
        ]
    if settings['shortlink']:
        btn.insert(0,
            [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", url=await get_shortlink(settings['url'], settings['api'], f'https://t.me/{temp.U_NAME}?start=all_{query.message.chat.id}_{key}')),
            InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs 📰", callback_data=f"languages#{key}#{req}#{offset}")]
        )
    else:
        btn.insert(0,
            [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", callback_data=f"send_all#{key}"),
            InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs 📰", callback_data=f"languages#{key}#{req}#{offset}")]
        )

    if 0 < offset <= MAX_BTN:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - MAX_BTN
        
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("« ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"{math.ceil(int(offset) / MAX_BTN) + 1}/{math.ceil(total / MAX_BTN)}", callback_data="buttons")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(int(offset) / MAX_BTN) + 1}/{math.ceil(total / MAX_BTN)}", callback_data="buttons"),
             InlineKeyboardButton("ɴᴇxᴛ »", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("« ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"{math.ceil(int(offset) / MAX_BTN) + 1}/{math.ceil(total / MAX_BTN)}", callback_data="buttons"),
                InlineKeyboardButton("ɴᴇxᴛ »", callback_data=f"next_{req}_{key}_{n_offset}")
            ]
        )
    btn.append(
        [InlineKeyboardButton("🚫 ᴄʟᴏsᴇ 🚫", callback_data="close_data")]
    )
    try:
        await query.message.edit_text(cap + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
    except MessageNotModified:
        pass

@Client.on_callback_query(filters.regex(r"^languages"))
async def languages_cb_handler(client: Client, query: CallbackQuery):
    _, key, req, offset = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴅᴏɴ'ᴛ ᴄʟɪᴄᴋ ᴏᴛʜᴇʀs ʀᴇsᴜʟᴛs !", show_alert=True)
    btn = [[
        InlineKeyboardButton(text=lang.title(), callback_data=f"lang_search#{lang}#{key}#{offset}#{req}"),
    ]
        for lang in LANGUAGES
    ]
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text("<b>ɪɴ ᴡʜɪᴄʜ ʟᴀɴɢᴜᴀɢᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ, sᴇʟᴇᴄᴛ ʜᴇʀᴇ</b>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^lang_search"))
async def filter_languages_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key, offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴅᴏɴ'ᴛ ᴄʟɪᴄᴋ ᴏᴛʜᴇʀs ʀᴇsᴜʟᴛs !", show_alert=True)

    search = BUTTONS.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nsᴇɴᴅ ɴᴇᴡ ʀᴇᴏ̨ᴜᴇsᴛ ᴀɢᴀɪɴ !", show_alert=True)
        return 

    files, l_offset, total_results = await get_search_results(search, lang=lang)
    if not files:
        await query.answer(f"sᴏʀʀʏ '{lang.title()}' ʟᴀɴɢᴜᴀɢᴇ ꜰɪʟᴇs ɴᴏᴛ ꜰᴏᴜɴᴅ 😕", show_alert=1)
        return
    temp.FILES[key] = files
    settings = await get_settings(query.message.chat.id)
    del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    files_link = ''

    if settings['links']:
        btn = []
        for file_num, file in enumerate(files, start=1):
            files_link += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {file.file_name}</a></b>"""
    else:
        btn = [[
            InlineKeyboardButton(text=f"📂 {get_size(file.file_size)} {file.file_name}", callback_data=f'file#{file.file_id}')
        ]
            for file in files
        ]
    if settings['shortlink']:
        btn.insert(0,
            [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", url=await get_shortlink(settings['url'], settings['api'], f'https://t.me/{temp.U_NAME}?start=all_{query.message.chat.id}_{key}'))]
        )
    else:
        btn.insert(0,
            [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", callback_data=f"send_all#{key}")]
        )
    
    if l_offset != "":
        btn.append(
            [InlineKeyboardButton(text=f"1/{math.ceil(int(total_results) / MAX_BTN)}", callback_data="buttons"),
             InlineKeyboardButton(text="ɴᴇxᴛ »", callback_data=f"lang_next#{req}#{key}#{lang}#{l_offset}#{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🚸 ɴᴏ ᴍᴏʀᴇ ᴘᴀɢᴇs 🚸", callback_data="buttons")]
        )
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text(cap + files_link + del_msg, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^lang_next"))
async def lang_next_page(bot, query):
    ident, req, key, lang, l_offset, offset = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴅᴏɴ'ᴛ ᴄʟɪᴄᴋ ᴏᴛʜᴇʀs ʀᴇsᴜʟᴛs !", show_alert=True)

    try:
        l_offset = int(l_offset)
    except:
        l_offset = 0

    search = BUTTONS.get(key)
    cap = CAP.get(key)
    settings = await get_settings(query.message.chat.id)
    del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    if not search:
        await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nsᴇɴᴅ ɴᴇᴡ ʀᴇᴏ̨ᴜᴇsᴛ ᴀɢᴀɪɴ !", show_alert=True)
        return 

    files, n_offset, total = await get_search_results(search, offset=l_offset, lang=lang)
    if not files:
        return
    temp.FILES[key] = files
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    files_link = ''

    if settings['links']:
        btn = []
        for file_num, file in enumerate(files, start=l_offset+1):
            files_link += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {file.file_name}</a></b>"""
    else:
        btn = [[
            InlineKeyboardButton(text=f"✨ {get_size(file.file_size)} ⚡️ {file.file_name}", callback_data=f'file#{file.file_id}')
        ]
            for file in files
        ]
    if settings['shortlink']:
        btn.insert(0,
            [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", url=await get_shortlink(settings['url'], settings['api'], f'https://t.me/{temp.U_NAME}?start=all_{query.message.chat.id}_{key}'))]
        )
    else:
        btn.insert(0,
            [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", callback_data=f"send_all#{key}")]
        )

    if 0 < l_offset <= MAX_BTN:
        b_offset = 0
    elif l_offset == 0:
        b_offset = None
    else:
        b_offset = l_offset - MAX_BTN

    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("« ʙᴀᴄᴋ", callback_data=f"lang_next#{req}#{key}#{lang}#{b_offset}#{offset}"),
             InlineKeyboardButton(f"{math.ceil(int(l_offset) / MAX_BTN) + 1}/{math.ceil(total / MAX_BTN)}", callback_data="buttons")]
        )
    elif b_offset is None:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(int(l_offset) / MAX_BTN) + 1}/{math.ceil(total / MAX_BTN)}", callback_data="buttons"),
             InlineKeyboardButton("ɴᴇxᴛ »", callback_data=f"lang_next#{req}#{key}#{lang}#{n_offset}#{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton("« ʙᴀᴄᴋ", callback_data=f"lang_next#{req}#{key}#{lang}#{b_offset}#{offset}"),
             InlineKeyboardButton(f"{math.ceil(int(l_offset) / MAX_BTN) + 1}/{math.ceil(total / MAX_BTN)}", callback_data="buttons"),
             InlineKeyboardButton("ɴᴇxᴛ »", callback_data=f"lang_next#{req}#{key}#{lang}#{n_offset}#{offset}")]
        )
    btn.append([InlineKeyboardButton(text="⪻ ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴘᴀɢᴇ", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text(cap + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)

@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, id, user = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴅᴏɴ'ᴛ ᴄʟɪᴄᴋ ᴏᴛʜᴇʀs ʀᴇsᴜʟᴛs !", show_alert=True)

    movie = await get_poster(id, id=True)
    search = movie.get('title')
    await query.answer('ᴄʜᴇᴄᴋ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ...')
    files, offset, total_results = await get_search_results(search)
    if files:
        k = (search, files, offset, total_results)
        await auto_filter(bot, query, k)
    else:
        await bot.send_message(LOG_CHANNEL, script.NO_RESULT_TXT.format(query.message.chat.title, query.message.chat.id, query.from_user.mention, search))
        k = await query.message.edit(f"👋 ʜᴇʟʟᴏ {query.from_user.mention},\n\nɪ ᴅᴏɴ'ᴛ ғɪɴᴅ <b>'{search}'</b> ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ. 😔")
        await asyncio.sleep(60)
        await k.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
            
@Client.on_callback_query(filters.regex(r"^Upi"))
async def upi_payment_info(client, callback_query):
    cmd = callback_query.message
    btn = [[            
        InlineKeyboardButton("ᴘᴀʏᴍᴇɴᴛ ʀᴇᴄᴇɪᴘᴛ ʜᴇʀᴇ 🧾", user_id=admin)
    ]
        for admin in ADMINS
    ]
    btn.append(
        [
            InlineKeyboardButton("ᴏ̨ʀ ᴄᴏᴅᴇ", callback_data="qrcode_info") ,                   
            InlineKeyboardButton("ᴜᴘɪ ɪᴅ", callback_data="upiid_info")
        ]
    )
    btn.append(
        [            
            InlineKeyboardButton("⇚ ʙᴀᴄᴋ", callback_data="buy_premium")
        ]
    ) 
    reply_markup = InlineKeyboardMarkup(btn)
    await client.edit_message_media(
        cmd.chat.id, 
        cmd.id, 
        InputMediaPhoto('https://graph.org/file/012b0fd51192f9e6506c0.jpg')
    )
    
    await cmd.edit(
        f"<b>👋 ʜᴇʏ {cmd.from_user.mention},\n    \n⚜️ ᴘᴀʏ ᴀᴍᴍᴏᴜɴᴛ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ᴘʟᴀɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀꜱʜɪᴘ !\n\n💵 ᴜᴘɪ ɪᴅ - <code>{UPI_ID}</code>\n\n‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.</b>",
        reply_markup = reply_markup
    )

@Client.on_callback_query(filters.regex(r"^qrcode_info"))
async def qr_code_info(client, callback_query):
    cmd = callback_query.message
    btn = [[            
        InlineKeyboardButton("ᴘᴀʏᴍᴇɴᴛ ʀᴇᴄᴇɪᴘᴛ ʜᴇʀᴇ 🧾", user_id=admin)
    ]
        for admin in ADMINS
    ]
    btn.append(
        [InlineKeyboardButton("⇚ ʙᴀᴄᴋ", callback_data="Upi")]
    )
    reply_markup = InlineKeyboardMarkup(btn)
    await client.edit_message_media(
        cmd.chat.id, 
        cmd.id, 
        InputMediaPhoto(PAYMENT_QR)
    )
    await cmd.edit(
        f"<b>👋 ʜᴇʏ {cmd.from_user.mention},\n      \n⚜️ ᴘᴀʏ ᴀᴍᴍᴏᴜɴᴛ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ᴘʟᴀɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀꜱʜɪᴘ !\n\n‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.</b>",
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
            

@Client.on_callback_query(filters.regex(r"^upiid_info"))
async def upi_id_info(client, callback_query):
    cmd = callback_query.message
    btn = [[            
        InlineKeyboardButton("ᴘᴀʏᴍᴇɴᴛ ʀᴇᴄᴇɪᴘᴛ ʜᴇʀᴇ 🧾", user_id=admin)
    ]
        for admin in ADMINS
    ]
    btn.append(
        [InlineKeyboardButton("⇚ ʙᴀᴄᴋ", callback_data="Upi")]
    )
    reply_markup = InlineKeyboardMarkup(btn)
    await cmd.edit(
        f"<b>👋 ʜᴇʏ {cmd.from_user.mention},\n      \n⚜️ ᴘᴀʏ ᴀᴍᴍᴏᴜɴᴛ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ᴘʟᴀɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀꜱʜɪᴘ !\n\n‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.</b>\n\n💵 <code>{UPI_ID}</code>",
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        try:
            user = query.message.reply_to_message.from_user.id
        except:
            user = query.from_user.id
        if int(user) != 0 and query.from_user.id != int(user):
            return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ !", show_alert=True)
        await query.answer("ᴄʟᴏsᴇᴅ !")
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
  
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        user = query.message.reply_to_message.from_user.id
        if int(user) != 0 and query.from_user.id != int(user):
            return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴅᴏɴ'ᴛ ᴄʟɪᴄᴋ ᴏᴛʜᴇʀs ʀᴇsᴜʟᴛs !", show_alert=True)
        await query.answer(url=f"https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file_id}")
        
    elif query.data == "get_trail":
        user_id = query.from_user.id
        free_trial_status = await db.get_free_trial_status(user_id)
        if not free_trial_status:            
            await db.give_free_trail(user_id)
            new_text = "**ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ꜰʀᴇᴇ ᴛʀᴀɪʟ ꜰᴏʀ 5 ᴍɪɴᴜᴛᴇs ꜰʀᴏᴍ ɴᴏᴡ 😀\n\nआप अब से 5 मिनट के लिए निःशुल्क ट्रायल का उपयोग कर सकते हैं 😀**"        
            await query.message.edit_text(text=new_text)
            return
        else:
            new_text= "**🤣 ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴜsᴇᴅ ғʀᴇᴇ, ɴᴏᴡ ɴᴏ ᴍᴏʀᴇ ғʀᴇᴇ ᴛʀᴀɪʟs. ᴘʟᴇᴀsᴇ ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ғʀᴏᴍ ʜᴇʀᴇ, ᴏᴜʀ 👉 /plans**"
            await query.message.edit_text(text=new_text)
            return
            
    elif query.data == "buy_premium":
        btn = [[
            InlineKeyboardButton("🏦 ꜱᴇʟᴇᴄᴛ ᴘᴀʏᴍᴇɴᴛ ᴍᴏᴅᴇ 🏧", callback_data="Upi")
        ]]            
            
        reply_markup = InlineKeyboardMarkup(btn)
        await query.message.reply_photo(
            photo="https://graph.org/file/ea8423d123dd90e34e10c.jpg",
            caption="**⚡️ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ ɴᴏᴡ\n\n ╭━━━━━━━━╮\n    ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs\n  • ₹10 - 1 ᴅᴀʏ ( ᴛʀɪᴀʟ )\n  • ₹25 - 1 ᴡᴇᴇᴋ ( ᴛʀɪᴀʟ )\n  • ₹50 - 1 ᴍᴏɴᴛʜ\n  • ₹120 - 3 ᴍᴏɴᴛʜs\n  • ₹220 - 6 ᴍᴏɴᴛʜs\n  • ₹400 - 1 ᴍᴏɴᴛʜs\n╰━━━━━━━━╯\n\nᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs :-\n\n☆ ɴᴇᴡ / ᴏʟᴅ ᴍᴏᴠɪᴇ ᴀɴᴅ ᴛᴠ sᴇʀɪᴇs\n☆ ʜɪɢʜ ᴏ̨ᴜᴀʟɪᴛʏ ᴀᴠᴀɪʟᴀʙʟᴇ\n☆ ɢᴇᴛ ғɪʟᴇs ᴅɪʀᴇᴄᴛʟʏ \n☆ ʜɪɢʜ sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋs\n☆ ғᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ \n☆ ʀᴇᴏ̨ᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 1 ʜᴏᴜʀ ɪғ ᴀᴠᴀɪʟᴀʙʟᴇ.\n\n**",
            reply_markup=reply_markup
        )
        return 
                
    elif query.data.startswith("checksub"):
        ident, mc = query.data.split("#")
        settings = await get_settings(int(mc.split("_", 2)[1]))
        btn = await is_subscribed(client, query, settings['fsub'])
        if btn:
            await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", show_alert=True)
            btn.append(
                [InlineKeyboardButton("🔁 ᴛʀʏ ᴀɢᴀɪɴ 🔁", callback_data=f"checksub#{mc}")]
            )
            await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
            return
        await query.answer(url=f"https://t.me/{temp.U_NAME}?start={mc}")
        await query.message.delete()

    elif query.data.startswith("unmuteme"):
        ident, chatid = query.data.split("#")
        settings = await get_settings(int(chatid))
        btn = await is_subscribed(client, query, settings['fsub'])
        if btn:
           await query.answer("ᴋɪɴᴅʟʏ ᴊᴏɪɴ ɢɪᴠᴇɴ ᴄʜᴀɴɴᴇʟ ᴛᴏ ɢᴇᴛ ᴜɴᴍᴜᴛᴇ", show_alert=True)
        else:
            await client.unban_chat_member(query.message.chat.id, user_id)
            await query.answer("ᴜɴᴍᴜᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ !", show_alert=True)
   
    elif query.data == "buttons":
        await query.answer("⚠️")

    elif query.data == "instructions":
        await query.answer("ᴍᴏᴠɪᴇ ʀᴇᴏ̨ᴜᴇsᴛ ғᴏʀᴍᴀᴛ.\nᴇxᴀᴍᴘʟᴇ :\nBlack Adam ᴏʀ Black Adam 2022\n\nᴛᴠ sᴇʀɪᴇs ʀᴇᴏ̨ᴜᴇsᴛ ғᴏʀᴍᴀᴛ.\nᴇxᴀᴍᴘʟᴇ :\nLoki S01E01 ᴏʀ Loki S01 E01\n\nᴅᴏɴ'ᴛ ᴜsᴇ sʏᴍʙᴏʟs.", show_alert=True)

    
    elif query.data == "start":
        await query.answer('ᴡᴇʟᴄᴏᴍᴇ !')
        buttons = [[
            InlineKeyboardButton('⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
        ],[
            InlineKeyboardButton('🌿 ᴀʙᴏᴜᴛ', callback_data="my_about"),
            InlineKeyboardButton('👤 ᴏᴡɴᴇʀ', callback_data='my_owner')
        ],[
            InlineKeyboardButton('🍁 ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('🔐 ᴘʀᴇᴍɪᴜᴍ', callback_data='buy_premium')
        ],[
            InlineKeyboardButton('💰 ᴇᴀʀɴ ᴍᴏɴᴇʏ ʙʏ ʙᴏᴛ 💰', callback_data='earn')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, get_wish()),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "my_about":
        buttons = [[
            InlineKeyboardButton('📊 sᴛᴀᴛᴜs', callback_data='stats'),
            InlineKeyboardButton('🔋 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ', callback_data='source')
        ],[
            InlineKeyboardButton('« ʙᴀᴄᴋ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MY_ABOUT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "stats":
        if query.from_user.id not in ADMINS:
            return await query.answer("ᴀᴅᴍɪɴs ᴏɴʟʏ !", show_alert=True)
        files = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        u_size = get_size(await db.get_db_size())
        f_size = get_size(536870912 - await db.get_db_size())
        uptime = get_readable_time(time.time() - temp.START_TIME)
        buttons = [[
            InlineKeyboardButton('« ʙᴀᴄᴋ', callback_data='my_about')
        ]]
        await query.message.edit_text(script.STATUS_TXT.format(files, users, chats, u_size, f_size, uptime), reply_markup=InlineKeyboardMarkup(buttons)
        )
        
    elif query.data == "my_owner":
        buttons = [[
            InlineKeyboardButton(text=f"☎️ ᴄᴏɴᴛᴀᴄᴛ - {(await client.get_users(admin)).first_name}", user_id=admin)
        ]
            for admin in ADMINS
        ]
        buttons.append(
            [InlineKeyboardButton('« ʙᴀᴄᴋ', callback_data='start')]
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MY_OWNER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "earn":
        buttons = [[
            InlineKeyboardButton('‼️ ʜᴏᴡ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ sʜᴏʀᴛɴᴇʀ ‼️', callback_data='howshort')
        ],[
            InlineKeyboardButton('≼ ʙᴀᴄᴋ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EARN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "howshort":
        buttons = [[
            InlineKeyboardButton('≼ ʙᴀᴄᴋ', callback_data='earn')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HOW_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('ɢʀᴏᴜᴘ ᴄᴏᴍᴍᴀɴᴅs', callback_data='infinity_group_commands')
        ],[
            InlineKeyboardButton('ᴜsᴇʀs ᴄᴏᴍᴍᴀɴᴅs', callback_data='user_command'),
            InlineKeyboardButton('ᴀᴅᴍɪɴs ᴄᴏᴍᴍᴀɴᴅs', callback_data='admin_command')
        ],[
            InlineKeyboardButton('« ʙᴀᴄᴋ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT,
            reply_markup=reply_markup
        )

    elif query.data == "user_command":
        buttons = [[
            InlineKeyboardButton('« ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.USER_COMMAND_TXT,
            reply_markup=reply_markup
        )
        
    elif query.data == "admin_command":
        if query.from_user.id not in ADMINS:
            return await query.answer("ᴀᴅᴍɪɴs ᴏɴʟʏ !", show_alert=True)
        buttons = [[
            InlineKeyboardButton('« ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_COMMAND_TXT,
            reply_markup=reply_markup
        )
        
    elif query.data == "infinity_group_commands":
        buttons = [[
            InlineKeyboardButton('« ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GROUP_COMMAND_TXT,
            reply_markup=reply_markup
        )
        
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('≼ ʙᴀᴄᴋ', callback_data='my_about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        if not await is_check_admin(client, int(grp_id), userid):
            await query.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ !", show_alert=True)
            return

        if status == "True":
            await save_group_settings(int(grp_id), set_type, False)
            await query.answer("❌")
        else:
            await save_group_settings(int(grp_id), set_type, True)
            await query.answer("✅")

        settings = await get_settings(int(grp_id))

        if settings is not None:
            buttons = [[
                InlineKeyboardButton('ᴀᴜᴛᴏ ғɪʟᴛᴇʀ', callback_data=f'setgs#auto_filter#{settings["auto_filter"]}#{grp_id}'),
                InlineKeyboardButton('✅ ʏᴇs' if settings["auto_filter"] else '❌ ɴᴏ', callback_data=f'setgs#auto_filter#{settings["auto_filter"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ғɪʟᴇ sᴇᴄᴜʀᴇ', callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}'),
                InlineKeyboardButton('✅ ʏᴇs' if settings["file_secure"] else '❌ ɴᴏ', callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ɪᴍᴅʙ ᴘᴏsᴛᴇʀ', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}'),
                InlineKeyboardButton('✅ ʏᴇs' if settings["imdb"] else '❌ ɴᴏ', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}')
            ],[
                InlineKeyboardButton('sᴘᴇʟʟɪɴɢ ᴄʜᴇᴄᴋ', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}'),
                InlineKeyboardButton('✅ ʏᴇs' if settings["spell_check"] else '❌ ɴᴏ', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ', callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}'),
                InlineKeyboardButton(f'{get_readable_time(DELETE_TIME)}' if settings["auto_delete"] else '❌ ɴᴏ', callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ᴡᴇʟᴄᴏᴍᴇ', callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',),
                InlineKeyboardButton('✅ ʏᴇs' if settings["welcome"] else '❌ ɴᴏ', callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}'),
            ],[
                InlineKeyboardButton('sʜᴏʀᴛʟɪɴᴋ', callback_data=f'setgs#shortlink#{settings["shortlink"]}#{grp_id}'),
                InlineKeyboardButton('✅ ʏᴇs' if settings["shortlink"] else '❌ ɴᴏ', callback_data=f'setgs#shortlink#{settings["shortlink"]}#{grp_id}'),
            ],[
                InlineKeyboardButton('ʀᴇsᴜʟᴛ ᴘᴀɢᴇ', callback_data=f'setgs#links#{settings["links"]}#{str(grp_id)}'),
                InlineKeyboardButton('⛓ ʟɪɴᴋ' if settings["links"] else '🧲 ʙᴜᴛᴛᴏɴ', callback_data=f'setgs#links#{settings["links"]}#{str(grp_id)}')
            ],[
                InlineKeyboardButton('ғsᴜʙ', callback_data=f'setgs#is_fsub#{settings.get("is_fsub", IS_FSUB)}#{str(grp_id)}'),
                InlineKeyboardButton('✅ ᴏɴ' if settings.get("is_fsub", IS_FSUB) else '❌ ᴏғғ', callback_data=f'setgs#is_fsub#{settings.get("is_fsub", IS_FSUB)}#{str(grp_id)}')
            ],[
                InlineKeyboardButton('sᴛʀᴇᴀᴍ', callback_data=f'setgs#is_stream#{settings.get("is_stream", IS_STREAM)}#{str(grp_id)}'),
                InlineKeyboardButton('✅ ᴏɴ' if settings.get("is_stream", IS_STREAM) else '❌ ᴏғғ', callback_data=f'setgs#is_stream#{settings.get("is_stream", IS_STREAM)}#{str(grp_id)}')
            ],[
                InlineKeyboardButton('❌ ᴄʟᴏsᴇ ❌', callback_data='close_data')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
        else:
            await query.message.edit_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ !")
            
    elif query.data == "delete_all":
        files = await Media.count_documents()
        await query.answer('Deleting...')
        await Media.collection.drop()
        await query.message.edit_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {files} ғɪʟᴇs")
        
    elif query.data.startswith("delete"):
        _, query_ = query.data.split("_", 1)
        deleted = 0
        await query.message.edit('ᴅᴇʟᴇᴛɪɴɢ...')
        total, files = await delete_files(query_)
        async for file in files:
            await Media.collection.delete_one({'_id': file.file_id})
            deleted += 1
        await query.message.edit(f'ᴅᴇʟᴇᴛᴇᴅ {deleted} ғɪʟᴇs ɪɴ ʏᴏᴜʀ ᴅᴀᴛᴀʙᴀsᴇ ɪɴ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {query_}')
     
    elif query.data.startswith("send_all"):
        ident, key = query.data.split("#")
        user = query.message.reply_to_message.from_user.id
        if int(user) != 0 and query.from_user.id != int(user):
            return await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nᴅᴏɴ'ᴛ ᴄʟɪᴄᴋ ᴏᴛʜᴇʀs ʀᴇsᴜʟᴛs !", show_alert=True)
        
        files = temp.FILES.get(key)
        if not files:
            await query.answer(f"ʜᴇʟʟᴏ {query.from_user.first_name},\nsᴇɴᴅ ɴᴇᴡ ʀᴇᴏ̨ᴜᴇsᴛ ᴀɢᴀɪɴ !", show_alert=True)
            return        
        await query.answer(url=f"https://t.me/{temp.U_NAME}?start=all_{query.message.chat.id}_{key}")

    elif query.data == "unmute_all_members":
        if not await is_check_admin(client, query.message.chat.id, query.from_user.id):
            await query.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ !", show_alert=True)
            return
        users_id = []
        await query.message.edit("ᴜɴᴍᴜᴛᴇ ᴀʟʟ sᴛᴀʀᴛᴇᴅ ! ᴛʜɪs ᴘʀᴏᴄᴇss ᴍᴀʏʙᴇ ɢᴇᴛ sᴏᴍᴇ ᴛɪᴍᴇ...")
        try:
            async for member in client.get_chat_members(query.message.chat.id, filter=enums.ChatMembersFilter.RESTRICTED):
                users_id.append(member.user.id)
            for user_id in users_id:
                await client.unban_chat_member(query.message.chat.id, user_id)
        except Exception as e:
            await query.message.delete()
            await query.message.reply(f'sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.\n\n<code>{e}</code>')
            return
        await query.message.delete()
        if users_id:
            await query.message.reply(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴᴍᴜᴛᴇᴅ <code>{len(users_id)}</code> ᴜsᴇʀs.")
        else:
            await query.message.reply('ɴᴏᴛʜɪɴɢ ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴜsᴇʀs.')

    elif query.data == "unban_all_members":
        if not await is_check_admin(client, query.message.chat.id, query.from_user.id):
            await query.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ !", show_alert=True)
            return
        users_id = []
        await query.message.edit("ᴜɴʙᴀɴ ᴀʟʟ sᴛᴀʀᴛᴇᴅ ! ᴛʜɪs ᴘʀᴏᴄᴇss ᴍᴀʏʙᴇ ɢᴇᴛ sᴏᴍᴇ ᴛɪᴍᴇ...")
        try:
            async for member in client.get_chat_members(query.message.chat.id, filter=enums.ChatMembersFilter.BANNED):
                users_id.append(member.user.id)
            for user_id in users_id:
                await client.unban_chat_member(query.message.chat.id, user_id)
        except Exception as e:
            await query.message.delete()
            await query.message.reply(f'sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.\n\n<code>{e}</code>')
            return
        await query.message.delete()
        if users_id:
            await query.message.reply(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴʙᴀɴ <code>{len(users_id)}</code> ᴜsᴇʀs.")
        else:
            await query.message.reply('ɴᴏᴛʜɪɴɢ ᴛᴏ ᴜɴʙᴀɴ ᴜsᴇʀs.')

    elif query.data == "kick_muted_members":
        if not await is_check_admin(client, query.message.chat.id, query.from_user.id):
            await query.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ !", show_alert=True)
            return
        users_id = []
        await query.message.edit("ᴋɪᴄᴋ ᴍᴜᴛᴇᴅ ᴜsᴇʀs sᴛᴀʀᴛᴇᴅ ! ᴛʜɪs ᴘʀᴏᴄᴇss ᴍᴀʏʙᴇ ɢᴇᴛ sᴏᴍᴇ ᴛɪᴍᴇ...")
        try:
            async for member in client.get_chat_members(query.message.chat.id, filter=enums.ChatMembersFilter.RESTRICTED):
                users_id.append(member.user.id)
            for user_id in users_id:
                await client.ban_chat_member(query.message.chat.id, user_id, datetime.now() + timedelta(seconds=30))
        except Exception as e:
            await query.message.delete()
            await query.message.reply(f'sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.\n\n<code>{e}</code>')
            return
        await query.message.delete()
        if users_id:
            await query.message.reply(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ ᴍᴜᴛᴇᴅ <code>{len(users_id)}</code> ᴜsᴇʀs.")
        else:
            await query.message.reply('ɴᴏᴛʜɪɴɢ ᴛᴏ ᴋɪᴄᴋ ᴍᴜᴛᴇᴅ ᴜsᴇʀs.')

    elif query.data == "kick_deleted_accounts_members":
        if not await is_check_admin(client, query.message.chat.id, query.from_user.id):
            await query.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ !", show_alert=True)
            return
        users_id = []
        await query.message.edit("ᴋɪᴄᴋ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs sᴛᴀʀᴛᴇᴅ ! ᴛʜɪs ᴘʀᴏᴄᴇss ᴍᴀʏʙᴇ ɢᴇᴛ sᴏᴍᴇ ᴛɪᴍᴇ...")
        try:
            async for member in client.get_chat_members(query.message.chat.id):
                if member.user.is_deleted:
                    users_id.append(member.user.id)
            for user_id in users_id:
                await client.ban_chat_member(query.message.chat.id, user_id, datetime.now() + timedelta(seconds=30))
        except Exception as e:
            await query.message.delete()
            await query.message.reply(f'sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.\n\n<code>{e}</code>')
            return
        await query.message.delete()
        if users_id:
            await query.message.reply(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ ᴅᴇʟᴇᴛᴇᴅ <code>{len(users_id)}</code> ᴀᴄᴄᴏᴜɴᴛs.")
        else:
            await query.message.reply('ɴᴏᴛʜɪɴɢ ᴛᴏ ᴋɪᴄᴋ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs.')

async def ai_spell_check(wrong_name):
    async def search_movie(wrong_name):
        search_results = imdb.search_movie(wrong_name)
        movie_list = [movie['title'] for movie in search_results]
        return movie_list
    movie_list = await search_movie(wrong_name)
    if not movie_list:
        return
    for _ in range(5):
        closest_match = process.extractOne(wrong_name, movie_list)
        if not closest_match or closest_match[1] <= 80:
            return 
        movie = closest_match[0]
        files, offset, total_results = await get_search_results(movie)
        if files:
            return movie
        movie_list.remove(movie)
    return

async def delSticker(st):
    try:
        await st.delete()
    except:
        pass
        
async def auto_filter(client, msg, spoll=False):
    #thinkStc = ''
    #thinkStc = await msg.reply_sticker(sticker=random.choice(STICKERS_IDS))
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        search = message.text
        files, offset, total_results = await get_search_results(search)
        if not files:
            if settings["spell_check"]:
                #await delSticker(thinkStc)
                ai_sts = await msg.reply_text('<b>ᴀɪ ɪs ᴄʜᴇᴋɪɴɢ ғᴏʀ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ.</b>')
                is_misspelled = await ai_spell_check(search)
                if is_misspelled:
                    await ai_sts.edit(f"<b>ᴀɪ sᴜɢɢᴇsᴛᴇᴅ <code>{is_misspelled}</code>\nsᴏ ɪ'ᴍ sᴇᴀʀᴄʜɪɴɢ ғᴏʀ <code>{is_misspelled}</code></b>")
                    await asyncio.sleep(2)
                    msg.text = is_misspelled
                    await ai_sts.delete()
                    return await auto_filter(client, msg)
                #await delSticker(thinkStc)
                await ai_sts.delete()
                await advantage_spell_chok(msg)
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    if spoll:
        await msg.message.delete()
    req = message.from_user.id if message.from_user else 0
    key = f"{message.chat.id}-{message.id}"
    temp.FILES[key] = files
    BUTTONS[key] = search
    files_link = ""

    if settings['links']:
        btn = []
        for file_num, file in enumerate(files, start=1):
            files_link += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {file.file_name}</a></b>"""
    else:
        btn = [[
            InlineKeyboardButton(text=f"📂 {get_size(file.file_size)} {file.file_name}", callback_data=f'file#{file.file_id}')
        ]
            for file in files
        ]
    
    if offset != "":
        if settings['shortlink']:
            btn.insert(0,
                [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", url=await get_shortlink(settings['url'], settings['api'], f'https://t.me/{temp.U_NAME}?start=all_{message.chat.id}_{key}')),
                InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs 📰", callback_data=f"languages#{key}#{req}#0")]
            )
        else:
            btn.insert(0,
                [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", callback_data=f"send_all#{key}"),
                 InlineKeyboardButton("📰 ʟᴀɴɢᴜᴀɢᴇs 📰", callback_data=f"languages#{key}#{req}#0")]
            )

        btn.append(
            [InlineKeyboardButton(text=f"1/{math.ceil(int(total_results) / MAX_BTN)}", callback_data="buttons"),
             InlineKeyboardButton(text="ɴᴇxᴛ »", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        if settings['shortlink']:
            btn.insert(0,
                [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", url=await get_shortlink(settings['url'], settings['api'], f'https://t.me/{temp.U_NAME}?start=all_{message.chat.id}_{key}'))]
            )
        else:
            btn.insert(0,
                [InlineKeyboardButton("♻️ sᴇɴᴅ ᴀʟʟ ♻️", callback_data=f"send_all#{key}")]
            )
        btn.append(
            [InlineKeyboardButton(text="🚸 ɴᴏ ᴍᴏʀᴇ ᴘᴀɢᴇs 🚸", callback_data="buttons")]
        )
    btn.append(
        [InlineKeyboardButton("🚫 ᴄʟᴏsᴇ 🚫", callback_data="close_data")]
    )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>💭 ʜᴇʏ {message.from_user.mention},\n♻️ ʜᴇʀᴇ ɪ ꜰᴏᴜɴᴅ ꜰᴏʀ ʏᴏᴜʀ sᴇᴀʀᴄʜ {search}...</b>"
    CAP[key] = cap
    del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    if imdb and imdb.get('poster'):
        try:
            if settings["auto_delete"]:
                #await delSticker(thinkStc)
                k = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024] + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), quote=True)
                await asyncio.sleep(DELETE_TIME)
                await k.delete()
                try:
                    await message.delete()
                except:
                    pass
            else:
                #await delSticker(thinkStc)
                await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024] + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), quote=True)
                
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            if settings["auto_delete"]:
                #await delSticker(thinkStc)
                k = await message.reply_photo(photo=poster, caption=cap[:1024] + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), quote=True)
                await asyncio.sleep(DELETE_TIME)
                await k.delete()
                try:
                    await message.delete()
                except:
                    pass
            else:
                #await delSticker(thinkStc)
                await message.reply_photo(photo=poster, caption=cap[:1024] + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), quote=True)
                
        except Exception as e:
            if settings["auto_delete"]:
                #await delSticker(thinkStc)
                k = await message.reply_text(cap + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True, quote=True)
                await asyncio.sleep(DELETE_TIME)
                await k.delete()
                try:
                    await message.delete()
                except:
                    pass
            else:
                #await delSticker(thinkStc)
                await message.reply_text(cap + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True, quote=True)
    else:
        if settings["auto_delete"]:
            #await delSticker(thinkStc)
            k = await message.reply_text(cap + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True, quote=True)
            await asyncio.sleep(DELETE_TIME)
            await k.delete()
            try:
                await message.delete()
            except:
                pass
        else:
            #await delSticker(thinkStc)
            await message.reply_text(cap + files_link + del_msg, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True, quote=True)

async def advantage_spell_chok(message):
    search = message.text
    google_search = search.replace(" ", "+")
    btn = [[
        InlineKeyboardButton("⚠️ ɪɴsᴛʀᴜᴄᴛɪᴏɴs ⚠️", callback_data='instructions'),
        InlineKeyboardButton("🔎 sᴇᴀʀᴄʜ ɢᴏᴏɢʟᴇ 🔍", url=f"https://www.google.com/search?q={google_search}")
    ]]
    try:
        movies = await get_poster(search, bulk=True)
    except:
        n = await message.reply_photo(photo=random.choice(PICS), caption=script.NOT_FILE_TXT.format(message.from_user.mention, search), reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(60)
        await n.delete()
        try:
            await message.delete()
        except:
            pass
        return

    if not movies:
        n = await message.reply_photo(photo=random.choice(PICS), caption=script.NOT_FILE_TXT.format(message.from_user.mention, search), reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(60)
        await n.delete()
        try:
            await message.delete()
        except:
            pass
        return

    user = message.from_user.id if message.from_user else 0
    buttons = [[
        InlineKeyboardButton(text=movie.get('title'), callback_data=f"spolling#{movie.movieID}#{user}")
    ]
        for movie in movies
    ]
    buttons.append(
        [InlineKeyboardButton("🚫 ᴄʟᴏsᴇ 🚫", callback_data="close_data")]
    )
    s = await message.reply_photo(photo=random.choice(PICS), caption=f"👋 ʜᴇʟʟᴏ {message.from_user.mention},\n\nɪ ᴄᴏᴜʟᴅɴ'ᴛ ғɪɴᴅ ᴛʜᴇ <b>'{search}'</b> ʏᴏᴜ ʀᴇᴏ̨ᴜᴇsᴛᴇᴅ.\nsᴇʟᴇᴄᴛ ɪғ ʏᴏᴜ ᴍᴇᴀɴᴛ ᴏɴᴇ ᴏғ ᴛʜᴇsᴇ ? 👇", reply_markup=InlineKeyboardMarkup(buttons), reply_to_message_id=message.id)
    await asyncio.sleep(300)
    await s.delete()
    try:
        await message.delete()
    except:
        pass

