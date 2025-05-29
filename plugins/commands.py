import os
import logging
import random, string
import asyncio
import time
import datetime
import requests
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait, ButtonDataInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, delete_files
from database.users_chats_db import db
from info import STICKERS_IDS, SUPPORT_GROUP, INDEX_CHANNELS, ADMINS, IS_VERIFY, VERIFY_TUTORIAL, VERIFY_EXPIRE, TUTORIAL, SHORTLINK_API, SHORTLINK_URL, AUTH_CHANNEL, DELETE_TIME, SUPPORT_LINK, UPDATES_LINK, LOG_CHANNEL, PICS, PROTECT_CONTENT, IS_STREAM, IS_FSUB, PAYMENT_QR
from utils import get_settings, delayed_delete, get_size, is_subscribed, is_check_admin, get_shortlink, get_verify_status, update_verify_status, save_group_settings, temp, get_readable_time, get_wish, get_seconds

@Client.on_message(filters.command("ask") & filters.incoming) #add your support grp to use this
async def aiRes(_, message):
    if message.chat.id == SUPPORT_GROUP:
        asked = message.text.split(None, 1)[1]
        if not asked:
            return await message.reply("ᴀsᴋ sᴏᴍᴇᴛʜɪɴɢ ᴀғᴛᴇʀ ᴀsᴋ ᴄᴏᴍᴍᴀɴᴅ !")
        #thinkStc = await message.reply_sticker(sticker=random.choice(STICKERS_IDS))
        url = f"https://bisal-ai-api.vercel.app/biisal" 
        res = requests.post(url , data={'query' : asked})
        if res.status_code == 200:
            response = res.json().get("response")
            #await thinkStc.delete()
            await message.reply(f"<b>ʜᴇʏ {message.from_user.mention()},\n{response.lstrip() if response.startswith(' ') else response}</b>")
        else:
            #await thinkStc.delete()
            await message.reply("ᴍᴀᴜsᴀᴍ ᴋʜᴀʀᴀʙ ʜᴀɪ ! ᴛʜᴏᴅɪ ᴅᴇʀ ᴍᴇɪɴ ᴛʀʏ ᴋʀᴇ !\nᴏʀ ʀᴇᴘᴏʀᴛ ᴛᴏ ᴅᴇᴠᴇʟᴏᴘᴇʀ.")
    else:
        btn = [[
            InlineKeyboardButton('💡 ʀᴇᴏ̨ᴜᴇsᴛ ɢʀᴏᴜᴘ 💡', url=SUPPORT_LINK)
        ]]
        await message.reply(f"<b>ʜᴇʏ {message.from_user.mention},\n\nᴘʟᴇᴀsᴇ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʀᴇᴏ̨ᴜᴇsᴛ ɢʀᴏᴜᴘ.</b>", reply_markup=InlineKeyboardMarkup(btn))
        
@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    botid = client.me.id
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not await db.get_chat(message.chat.id):
            total = await client.get_chat_members_count(message.chat.id)
            username = f'@{message.chat.username}' if message.chat.username else 'Private'
            await client.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(message.chat.title, message.chat.id, username, total))       
            await db.add_chat(message.chat.id, message.chat.title)
        wish = get_wish()
        btn = [[
            InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ⚡️', url=UPDATES_LINK),
            InlineKeyboardButton('💡 ʀᴇᴏ̨ᴜᴇsᴛ ɢʀᴏᴜᴘ 💡', url=SUPPORT_LINK)
        ]]
        await message.reply(text=f"<b>ʜᴇʏ {message.from_user.mention}, <i>{wish}</i>\nʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ??</b>", reply_markup=InlineKeyboardMarkup(btn))
        return 
        
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.NEW_USER_TXT.format(message.from_user.mention, message.from_user.id))

    verify_status = await get_verify_status(message.from_user.id)
    if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
        await update_verify_status(message.from_user.id, is_verified=False)
    
    if (len(message.command) != 2) or (len(message.command) == 2 and message.command[1] == 'start'):
        buttons = [[
            InlineKeyboardButton('⤬ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('🌿 ᴀʙᴏᴜᴛ', callback_data="my_about"),
                    InlineKeyboardButton('👤 ᴏᴡɴᴇʀ', callback_data='my_owner')
                ],[
                    InlineKeyboardButton('🍁 ʜᴇʟᴘ', callback_data='help'),
                    InlineKeyboardButton('🔐 ᴘʀᴇᴍɪᴜᴍ', callback_data='buy_premium')
                ],[
                    InlineKeyboardButton('💰 ᴇᴀʀɴ ᴍᴏɴᴇʏ 💰', callback_data='earn')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, get_wish()),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return


    mc = message.command[1]

    if mc.startswith('verify'):
        _, token = mc.split("_", 1)
        verify_status = await get_verify_status(message.from_user.id)
        if verify_status['verify_token'] != token:
            return await message.reply("ʏᴏᴜʀ ᴠᴇʀɪғʏ ᴛᴏᴋᴇɴ ɪs ɪɴᴠᴀʟɪᴅ.")
        await update_verify_status(message.from_user.id, is_verified=True, verified_time=time.time())
        if verify_status["link"] == "":
            reply_markup = None
        else:
            btn = [[
                InlineKeyboardButton("📌 ɢᴇᴛ ғɪʟᴇ 📌", url=f'https://t.me/{temp.U_NAME}?start={verify_status["link"]}')
            ]]
            reply_markup = InlineKeyboardMarkup(btn)
        await message.reply(f"✅ ʏᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ ᴜɴᴛɪʟ : {get_readable_time(VERIFY_EXPIRE)}", reply_markup=reply_markup, protect_content=True)
        return
    
    verify_status = await get_verify_status(message.from_user.id)
    if not await db.has_premium_access(message.from_user.id):
        if IS_VERIFY and not verify_status['is_verified']:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            await update_verify_status(message.from_user.id, verify_token=token, link="" if mc == 'inline_verify' else mc)
            link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://t.me/{temp.U_NAME}?start=verify_{token}')
            btn = [[
                InlineKeyboardButton("🧿 ᴠᴇʀɪғʏ 🧿", url=link)
            ],[
                InlineKeyboardButton('🗳 ᴛᴜᴛᴏʀɪᴀʟ 🗳', url=VERIFY_TUTORIAL)
            ]]
            await message.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴅᴀʏ ! ᴋɪɴᴅʟʏ ᴠᴇʀɪғʏ ɴᴏᴡ. 🔐", reply_markup=InlineKeyboardMarkup(btn), protect_content=True)
            return
    else:
        pass

    settings = await get_settings(int(mc.split("_", 2)[1]))
    if settings.get('is_fsub', IS_FSUB):
        btn = await is_subscribed(client, message, settings['fsub'])
        if btn:
            btn.append(
                [InlineKeyboardButton("🔁 ᴛʀʏ ᴀɢᴀɪɴ 🔁", callback_data=f"checksub#{mc}")]
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await message.reply_photo(
                photo=random.choice(PICS),
                caption=f"👋 Hello {message.from_user.mention},\n\nᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ. 😇",
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            return 
        
    if mc.startswith('all'):
        _, grp_id, key = mc.split("_", 2)
        files = temp.FILES.get(key)
        if not files:
            return await message.reply('ɴᴏ sᴜᴄʜ ᴀʟʟ ғɪʟᴇ ᴇxɪsᴛ !')
        settings = await get_settings(int(grp_id))
        for file in files:
            CAPTION = settings['caption']
            f_caption = CAPTION.format(
                file_caption=files.caption or file.file_name
            )
            if settings.get('is_stream', IS_STREAM):
                btn = [[
                    InlineKeyboardButton("✛ ᴡᴀᴛᴄʜ & ᴅᴏᴡɴʟᴏᴀᴅ ✛", callback_data=f"stream#{file.file_id}")
                ],[
                    InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs ⚡️', url=UPDATES_LINK),
                    InlineKeyboardButton('💡 ʀᴇᴏ̨ᴜᴇsᴛ 💡', url=SUPPORT_LINK)
                ],[
                    InlineKeyboardButton('⁉️ ᴄʟᴏsᴇ ⁉️', callback_data='close_data')
                ]]
            else:
                btn = [[
                    InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs ⚡️', url=UPDATES_LINK),
                    InlineKeyboardButton('💡 ʀᴇᴏ̨ᴜᴇsᴛ 💡', url=SUPPORT_LINK)
                ],[
                    InlineKeyboardButton('⁉️ ᴄʟᴏsᴇ ⁉️', callback_data='close_data')
                ]]
            sent_message = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file.file_id,
                caption=f_caption,
                protect_content=settings['file_secure'],
                reply_markup=InlineKeyboardMarkup(btn)
            )
            asyncio.create_task(delayed_delete(client, sent_message, 600))
        await message.reply("<b>ᴛʜɪs ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀғᴛᴇʀ 10 ᴍɪɴ sᴏ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ɪᴛ ɪɴ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs.</b>")                                   
        return

    type_, grp_id, file_id = mc.split("_", 2)
    files_ = await get_file_details(file_id)
    if not files_:
        return await message.reply('No Such File Exist!')
    files = files_[0]
    settings = await get_settings(int(grp_id))
    if type_ != 'shortlink' and settings['shortlink']:
        if not await db.has_premium_access(message.from_user.id):
            link = await get_shortlink(settings['url'], settings['api'], f"https://t.me/{temp.U_NAME}?start=shortlink_{grp_id}_{file_id}")
            btn = [[
                InlineKeyboardButton("♻️ ɢᴇᴛ ғɪʟᴇ ♻️", url=link)
            ],[
                InlineKeyboardButton("📍 ʜᴏᴡ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ 📍", url=settings['tutorial'])
            ]]
            await message.reply(f"[{get_size(files.file_size)}] {files.file_name}\n\nʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ, ᴘʟᴇᴀsᴇ ɢᴇᴛ ᴜsɪɴɢ ᴛʜɪs ʟɪɴᴋ. 👍", reply_markup=InlineKeyboardMarkup(btn), protect_content=True)
            return
    else:
        pass
        
    CAPTION = settings['caption']
    f_caption = CAPTION.format(
        file_caption=files.caption or file.file_name
    )
    if settings.get('is_stream', IS_STREAM):
        btn = [[
            InlineKeyboardButton("✛ ᴡᴀᴛᴄʜ & ᴅᴏᴡɴʟᴏᴀᴅ ✛", callback_data=f"stream#{file_id}")
        ],[
            InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs ⚡️', url=UPDATES_LINK),
            InlineKeyboardButton('💡 ʀᴇᴏ̨ᴜᴇsᴛ 💡', url=SUPPORT_LINK)
        ],[
            InlineKeyboardButton('⁉️ ᴄʟᴏsᴇ ⁉️', callback_data='close_data')
        ]]
    else:
        btn = [[
            InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs ⚡️', url=UPDATES_LINK),
            InlineKeyboardButton('💡 ʀᴇᴏ̨ᴜᴇsᴛ 💡', url=SUPPORT_LINK)
        ],[
            InlineKeyboardButton('⁉️ ᴄʟᴏsᴇ ⁉️', callback_data='close_data')
        ]]
    sent_message = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=settings['file_secure'],
        reply_markup=InlineKeyboardMarkup(btn)
    )
    await sent_message.reply("<b>ᴛʜɪs ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀғᴛᴇʀ 10 ᴍɪɴ sᴏ ᴘʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ɪᴛ ɪɴ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs.</b>")
    asyncio.create_task(delayed_delete(client, sent_message, 600))

@Client.on_message(filters.command('index_channels') & filters.user(ADMINS))
async def channels_info(bot, message):
    """sᴇɴᴅ ʙᴀsɪᴄ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏғ ɪɴᴅᴇx ᴄʜᴀɴɴᴇʟs"""
    ids = INDEX_CHANNELS
    if not ids:
        return await message.reply("ɴᴏᴛ sᴇᴛ INDEX_CHANNELS")

    text = '**ɪɴᴅᴇxᴇᴅ ᴄʜᴀɴɴᴇʟs :**\n\n'
    for id in ids:
        chat = await bot.get_chat(id)
        text += f'{chat.title}\n'
    text += f'\n**ᴛᴏᴛᴀʟ :** {len(ids)}'
    await message.reply(text)

@Client.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot, message):
    msg = await message.reply('ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...')
    files = await Media.count_documents()
    users = await db.total_users_count()
    chats = await db.total_chat_count()
    u_size = get_size(await db.get_db_size())
    f_size = get_size(536870912 - await db.get_db_size())
    uptime = get_readable_time(time.time() - temp.START_TIME)
    await msg.edit(script.STATUS_TXT.format(files, users, chats, u_size, f_size, uptime))    
    
@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")
    grp_id = message.chat.id
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
    settings = await get_settings(grp_id)
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
        await message.reply_text(
            text=f"ᴄʜᴀɴɢᴇ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ғᴏʀ <b>'{message.chat.title}'</b> ᴀs ʏᴏᴜʀ ᴡɪsʜ. ⚙",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    else:
        await message.reply_text('sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ !')

@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")      
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
    try:
        template = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !")   
    await save_group_settings(grp_id, 'template', template)
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴛᴇᴍᴘʟᴀᴛᴇ ғᴏʀ {title} ᴛᴏ\n\n{template}")  
    
@Client.on_message(filters.command('set_caption'))
async def save_caption(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")      
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !") 
    await save_group_settings(grp_id, 'caption', caption)
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴄᴀᴘᴛɪᴏɴ ғᴏʀ {title} ᴛᴏ\n\n{caption}")
        
@Client.on_message(filters.command('set_shortlink'))
async def save_shortlink(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")    
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
    try:
        _, url, api = message.text.split(" ", 2)
    except:
        return await message.reply_text("<b>ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ :-\n\nɢɪᴠᴇ ᴍᴇ ᴀ sʜᴏʀᴛʟɪɴᴋ & ᴀᴘɪ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ...\n\nᴇx :- <code>/shortlink mdisklink.link 5843c3cc645f5077b2200a2c77e0344879880b3e</code>")   
    try:
        await get_shortlink(url, api, f'https://t.me/{temp.U_NAME}')
    except:
        return await message.reply_text("ʏᴏᴜʀ sʜᴏʀᴛʟɪɴᴋ ᴀᴘɪ ᴏʀ ᴜʀʟ ɪɴᴠᴀʟɪᴅ, ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ !")   
    await save_group_settings(grp_id, 'url', url)
    await save_group_settings(grp_id, 'api', api)
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ sʜᴏʀᴛʟɪɴᴋ ғᴏʀ {title} ᴛᴏ\n\nᴜʀʟ - {url}\nᴀᴘɪ - {api}")
    
@Client.on_message(filters.command('get_custom_settings'))
async def get_custom_settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ...')    
    settings = await get_settings(grp_id)
    text = f"""ᴄᴜsᴛᴏᴍ sᴇᴛᴛɪɴɢs ғᴏʀ : {title}

sʜᴏʀᴛʟɪɴᴋ ᴜʀʟ : {settings["url"]}
sʜᴏʀᴛʟɪɴᴋ ᴀᴘɪ : {settings["api"]}

ɪᴍᴅʙ ᴛᴇᴍᴘʟᴀᴛᴇ : {settings['template']}

ғɪʟᴇ ᴄᴀᴘᴛɪᴏɴ : {settings['caption']}

ᴡᴇʟᴄᴏᴍᴇ ᴛᴇxᴛ : {settings['welcome_text']}

ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ : {settings['tutorial']}

ғᴏʀᴄᴇ ᴄʜᴀɴɴᴇʟs : {str(settings['fsub'])[1:-1] if settings['fsub'] else 'ɴᴏᴛ sᴇᴛ'}"""

    btn = [[
        InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close_data")
    ]]
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)

@Client.on_message(filters.command('set_welcome'))
async def save_welcome(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")      
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
    try:
        welcome = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !")    
    await save_group_settings(grp_id, 'welcome_text', welcome)
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ғᴏʀ {title} ᴛᴏ\n\n{welcome}")
        
@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete_file(bot, message):
    try:
        query = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !\nᴜsᴀɢᴇ : /delete ᴏ̨ᴜᴇʀʏ")
    msg = await message.reply_text('sᴇᴀʀᴄʜɪɴɢ...')
    total, files = await delete_files(query)
    if int(total) == 0:
        return await msg.edit('ɴᴏᴛ ʜᴀᴠᴇ ғɪʟᴇs ɪɴ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ')
    btn = [[
        InlineKeyboardButton("ʏᴇs", callback_data=f"delete_{query}")
    ],[
        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close_data")
    ]]
    await msg.edit(f"ᴛᴏᴛᴀʟ {total} ғɪʟᴇs ғᴏᴜɴᴅ ɪɴ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {query}.\n\nᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ?", reply_markup=InlineKeyboardMarkup(btn))
 
@Client.on_message(filters.command('delete_all') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    btn = [[
        InlineKeyboardButton(text="ʏᴇs", callback_data="delete_all")
    ],[
        InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close_data")
    ]]
    files = await Media.count_documents()
    if int(files) == 0:
        return await message.reply_text('ɴᴏᴛ ʜᴀᴠᴇ ғɪʟᴇs ᴛᴏ ᴅᴇʟᴇᴛᴇ')
    await message.reply_text(f'ᴛᴏᴛᴀʟ {files} ғɪʟᴇs ʜᴀᴠᴇ.\nᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ?', reply_markup=InlineKeyboardMarkup(btn))

@Client.on_message(filters.command('set_tutorial'))
async def set_tutorial(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")       
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
    try:
        tutorial = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !")   
    await save_group_settings(grp_id, 'tutorial', tutorial)
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴛᴜᴛᴏʀɪᴀʟ ғᴏʀ {title} ᴛᴏ\n\n{tutorial}")

@Client.on_message(filters.command('set_fsub'))
async def set_fsub(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ !</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.")      
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
    vp = message.text.split(" ", 1)[1]
    if vp.lower() in ["Off", "off", "False", "false", "Turn Off", "turn off"]:
        await save_group_settings(grp_id, 'is_fsub', False)
        return await message.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ ᴛᴜʀɴᴇᴅ ᴏғғ !")
    elif vp.lower() in ["On", "on", "True", "true", "Turn On", "turn on"]:
        await save_group_settings(grp_id, 'is_fsub', True)
        return await message.reply_text("sᴜᴄᴄᴇssғᴜʟʟʏ ᴛᴜʀɴᴇᴅ ᴏɴ !")
    try:
        ids = message.text.split(" ", 1)[1]
        fsub_ids = list(map(int, ids.split()))
    except IndexError:
        return await message.reply_text("ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !\n\nᴄᴀɴ ᴍᴜʟᴛɪᴘʟᴇ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅ, sᴇᴘᴀʀᴀᴛᴇ ʙʏ sᴘᴀᴄᴇs. ʟɪᴋᴇ : /set_fsub ɪᴅ1 ɪᴅ2 ɪᴅ3")
    except ValueError:
        return await message.reply_text('ᴍᴀᴋᴇ sᴜʀᴇ ɪᴅ ɪs ɪɴᴛᴇɢᴇʀ.')        
    channels = "ᴄʜᴀɴɴᴇʟs :\n"
    for id in fsub_ids:
        try:
            chat = await client.get_chat(id)
        except Exception as e:
            return await message.reply_text(f"{id} ɪs ɪɴᴠᴀʟɪᴅ !\nᴍᴀᴋᴇ sᴜʀᴇ ᴛʜɪs ʙᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ.\n\nᴇʀʀᴏʀ - {e}")
        if chat.type != enums.ChatType.CHANNEL:
            return await message.reply_text(f"{id} ɪs ɴᴏᴛ ᴄʜᴀɴɴᴇʟ.")
        channels += f'{chat.title}\n'
    await save_group_settings(grp_id, 'fsub', fsub_ids)
    await message.reply_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ғᴏʀᴄᴇ ᴄʜᴀɴɴᴇʟs ғᴏʀ {title} ᴛᴏ\n\n{channels}")

@Client.on_message(filters.command('ping'))
async def ping(client, message):
    start_time = time.monotonic()
    msg = await message.reply("👀")
    end_time = time.monotonic()
    await msg.edit(f'{round((end_time - start_time) * 1000)} ᴍs')
    
@Client.on_message(filters.command("add_premium"))
async def give_premium_cmd_handler(client, message):
    if message.from_user.id not in ADMINS:
        return
    if len(message.command) == 3:
        user_id = int(message.command[1])  # Convert the user_id to integer
        time = message.command[2]        
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time} 
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            await message.reply_text("ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ.")
            
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ꜰᴏʀ {time} ᴇɴᴊᴏʏ 😀\n</b>",                
            )
        else:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴜsᴇ '1day ғᴏʀ ᴅᴀʏs', '1hour ғᴏʀ ʜᴏᴜʀs', '1min ғᴏʀ ᴍɪɴᴜᴛᴇs', '1month ғᴏʀ ᴍᴏɴᴛʜs', '1year ғᴏʀ ʏᴇᴀʀs'")
    else:
        await message.reply_text("<b>ᴜsᴀɢᴇ : /add_premium ᴜsᴇʀɪᴅ ᴛɪᴍᴇ \n\nᴇxᴀᴍᴘʟᴇ /add_premium 1234567 10day \n\n( ᴇ.ɢ. ғᴏʀ ᴛɪᴍᴇ ᴜɴɪᴛs '1day ғᴏʀ ᴅᴀʏs', '1hour ғᴏʀ ʜᴏᴜʀs', '1min ғᴏʀ ᴍɪɴᴜᴛᴇs', '1month ғᴏʀ ᴍᴏɴᴛʜs', '1year ғᴏʀ ʏᴇᴀʀs' )</b>")
        
@Client.on_message(filters.command("remove_premium"))
async def remove_premium_cmd_handler(client, message):
    if message.from_user.id not in ADMINS:
        return
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convert the user_id to integer
      #  time = message.command[2]
        time = "1s"
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  # Using "id" instead of "user_id"
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            await message.reply_text("ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʀᴇᴍᴏᴠᴇᴅ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ.")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇᴅ ʙʏ ᴀᴅᴍɪɴs \n\n ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ɪғ ᴛʜɪs ɪs ᴍɪsᴛᴀᴋᴇ \n\n 👮 ᴀᴅᴍɪɴ : @cntct_7bot \n</b>",                
            )
        else:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ғᴏʀᴍᴀᴛ.'")
    else:
        await message.reply_text("ᴜsᴀɢᴇ: /remove_premium ᴜsᴇʀɪᴅ")
        
@Client.on_message(filters.command("plans"))
async def plans_cmd_handler(client, message):                
    btn = [            
        [InlineKeyboardButton("ꜱᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ʀᴇᴄᴇɪᴘᴛ 🧾", url="https://t.me/cntct_7bot")],
        [InlineKeyboardButton("⚠️ ᴄʟᴏsᴇ / ᴅᴇʟᴇᴛᴇ ⚠️", callback_data="close_data")]
    ]
    reply_markup = InlineKeyboardMarkup(btn)
    await message.reply_photo(
        photo=PAYMENT_QR,
        caption="**ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs 🎁\n\n☆ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪғʏ\n☆ ᴀᴅ ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n☆ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇ ᴀɴᴅ ᴛᴠ sᴇʀɪᴇs",
        reply_markup=reply_markup
    )
        
@Client.on_message(filters.command("my_plan"))
async def check_plans_cmd(client, message):
    user_id  = message.from_user.id
    if await db.has_premium_access(user_id):         
        remaining_time = await db.check_remaining_uasge(user_id)             
        expiry_time = remaining_time + datetime.datetime.now()
        await message.reply_text(f"**ʏᴏᴜʀ ᴘʟᴀɴs ᴅᴇᴛᴀɪʟs ᴀʀᴇ :\n\nʀᴇᴍᴀɪɴɪɴɢ ᴛɪᴍᴇ : {remaining_time}\n\nᴇxᴘɪʀᴇ ᴛɪᴍᴇ : {expiry_time}**")
    else:
        btn = [ 
            [InlineKeyboardButton("ɢᴇᴛ ғʀᴇᴇ ᴛʀᴀɪʟ ғᴏʀ 𝟻 ᴍɪɴᴜᴛᴇꜱ ☺️", callback_data="get_trail")],
            [InlineKeyboardButton("ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ : ʀᴇᴍᴏᴠᴇ ᴀᴅs", callback_data="buy_premium")],
            [InlineKeyboardButton("⚠️ ᴄʟᴏsᴇ / ᴅᴇʟᴇᴛᴇ ⚠️", callback_data="close_data")]
        ]
        reply_markup = InlineKeyboardMarkup(btn)
        m=await message.reply_sticker("CAACAgIAAxkBAAIBTGVjQbHuhOiboQsDm35brLGyLQ28AAJ-GgACglXYSXgCrotQHjibHgQ")         
        await message.reply_text(f"**😢 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ sᴜʙsᴄʀɪᴘᴛɪᴏɴ.\n\n ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ /plans**",reply_markup=reply_markup)
        await asyncio.sleep(2)
        await m.delete()
