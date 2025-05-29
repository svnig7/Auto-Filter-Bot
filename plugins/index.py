# (c) github - @Rishikesh-Sharma09 ,telegram - https://telegram.me/Rk_botz
# removing credits doesn't make you coder 
# New better way of indexing and skipping added 
import logging
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified, UserIsBlocked
from info import ADMINS, LOG_CHANNEL, INDEX_EXTENSIONS
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from utils import temp, get_readable_time
import re, time

lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    _, ident, chat, lst_msg_id, skip = query.data.split("#")
    if ident == 'yes':
        msg = query.message
        await msg.edit("sᴛᴀʀᴛɪɴɢ ɪɴᴅᴇxɪɴɢ...")
        try:
            chat = int(chat)
        except:
            chat = chat
        await index_files_to_db(int(lst_msg_id), chat, msg, bot, int(skip))
    elif ident == 'cancel':
        temp.CANCEL = True
        await query.message.edit("ᴛʀʏɪɴɢ ᴛᴏ ᴄᴀɴᴄᴇʟ ɪɴᴅᴇxɪɴɢ...")

@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('ᴛʜɪs ᴍᴀʏ ʙᴇ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟ / ɢʀᴏᴜᴘ. ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ ᴏᴠᴇʀ ᴛʜᴇʀᴇ ᴛᴏ ɪɴᴅᴇx ᴛʜᴇ ғɪʟᴇs.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ sᴘᴇᴄɪғɪᴇᴅ.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'ᴇʀʀᴏʀs - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴀᴛ ɪ ᴀᴍ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ, ɪғ ᴄʜᴀɴɴᴇʟ ɪs ᴘʀɪᴠᴀᴛᴇ')
    if k.empty:
        return await message.reply('ᴛʜɪs ᴍᴀʏ ʙᴇ ɢʀᴏᴜᴘ ᴀɴᴅ ɪ ᴀᴍ ɴᴏᴛ ᴀ ᴀᴅᴍɪɴ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ.')

    s = await message.reply_text(
        text = "<b>sᴇɴᴅ ᴛʜᴇ sᴋɪᴘ ᴍᴇssᴀɢᴇ ɴᴜᴍʙᴇʀ.\n\nɪғ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ᴛᴏ sᴋɪᴘ ᴀɴʏ ғɪʟᴇs sᴇɴᴅ ᴍᴇ 👉 0 \n</b>",
        reply_to_message_id=message.id,
        reply_markup=ForceReply(True)
    )

@Client.on_message(filters.private & filters.reply) 
async def forceskip(client, message):      
    reply_message = message.reply_to_message
    msg = None  # Initialize msg to avoid UnboundLocalError

    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):   
        skip_msg = message
        try:
            skip = int(skip_msg.text)
        except:
            await message.reply("ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ᴘʀᴏᴠɪᴅᴇᴅ ᴜsɪɴɢ 0 ᴀs ᴀ sᴋɪᴘ ɴᴜᴍʙᴇʀ")
            skip = 0

        msg = await client.get_messages(message.chat.id, reply_message.id) 
        info = msg.reply_to_message

        if info.text:
            regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
            match = regex.match(info.text)
            if not match:
                return await info.reply('ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ')

            chat_id = match.group(4)
            last_msg_id = int(match.group(5))

            if chat_id.isnumeric():
                chat_id = int("-100" + chat_id)

        elif info.forward_from_chat and info.forward_from_chat.type == enums.ChatType.CHANNEL:
            last_msg_id = info.forward_from_message_id
            chat_id = info.forward_from_chat.username or info.forward_from_chat.id
        else:
            return

        # Proceed only if everything was parsed correctly
        if message.from_user.id in ADMINS:      
            buttons = [
                [InlineKeyboardButton('ʏᴇs', callback_data=f'index#yes#{chat_id}#{last_msg_id}#{skip}')],
                [InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data='close_data')]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)

            # Clean up messages
            await message.delete()
            if msg:
                await msg.delete()

            return await message.reply(
                f'ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɪɴᴅᴇx ᴛʜɪs ᴄʜᴀɴɴᴇʟ / ɢʀᴏᴜᴘ ?\n\n'
                f'ᴄʜᴀᴛ ɪᴅ / ᴜsᴇʀɴᴀᴍᴇ : <code>{chat_id}</code>\n'
                f'ʟᴀsᴛ ᴍᴇssᴀɢᴇ ɪᴅ : <code>{last_msg_id}</code>',
                reply_markup=reply_markup
            )

    else:
        await message.reply("ɴᴏ ᴠᴀʟɪᴅ ʀᴇᴘʟʏ ғᴏᴜɴᴅ.")

async def index_files_to_db(lst_msg_id, chat, msg, bot, skip):
    start_time = time.time()
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    current = skip
    
    async with lock:
        try:
            async for message in bot.iter_messages(chat, lst_msg_id, skip):
                time_taken = get_readable_time(time.time()-start_time)
                if temp.CANCEL:
                    temp.CANCEL = False
                    await msg.edit(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴄᴀɴᴄᴇʟʟᴇᴅ !\nᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ {time_taken}\n\nsᴀᴠᴇᴅ <code>{total_files}</code> ғɪʟᴇs ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ !\nᴅᴜᴘʟɪᴄᴀᴛᴇ ғɪʟᴇs sᴋɪᴘᴘᴇᴅ : <code>{duplicate}</code>\nᴅᴇʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ : <code>{deleted}</code>\nɴᴏɴ-ᴍᴇᴅɪᴀ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ : <code>{no_media + unsupported}</code>\nᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ : <code>{unsupported}</code>\nᴇʀʀᴏʀs ᴏᴄᴄᴜʀʀᴇᴅ : <code>{errors}</code>")
                    return
                current += 1
                if current % 60 == 0:
                    btn = [[
                        InlineKeyboardButton('ᴄᴀɴᴄᴇʟ', callback_data=f'index#cancel#{chat}#{lst_msg_id}#{skip}')
                    ]]
                    await msg.edit_text(text=f"ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs ʀᴇᴄᴇɪᴠᴇᴅ : <code>{current}</code>\nᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs sᴀᴠᴇᴅ : <code>{total_files}</code>\nᴅᴜᴘʟɪᴄᴀᴛᴇ ғɪʟᴇs sᴋɪᴘᴘᴇᴅ : <code>{duplicate}</code>\nᴅᴇʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ : <code>{deleted}</code>\nɴᴏɴ-ᴍᴇᴅɪᴀ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ : <code>{no_media + unsupported}</code>\nᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ : <code>{unsupported}</code>\nᴇʀʀᴏʀs ᴏᴄᴄᴜʀʀᴇᴅ : <code>{errors}</code>", reply_markup=InlineKeyboardMarkup(btn))
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                elif not (str(media.file_name).lower()).endswith(tuple(INDEX_EXTENSIONS)):
                    unsupported += 1
                    continue
                media.caption = message.caption
                sts = await save_file(message, media)
                if sts == 'suc':
                    total_files += 1
                elif sts == 'dup':
                    duplicate += 1
                elif sts == 'err':
                    errors += 1
        except Exception as e:
            await msg.reply(f'ɪɴᴅᴇx ᴄᴀɴᴄᴇʟᴇᴅ ᴅᴜᴇ ᴛᴏ ᴇʀʀᴏʀ - {e}')
        else:
            await msg.edit(f'sᴜᴄᴄᴇsғᴜʟʟʏ sᴀᴠᴇᴅ <code>{total_files}</code> ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ !\nᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ {time_taken}\n\nᴅᴜᴘʟɪᴄᴀᴛᴇ ғɪʟᴇs sᴋɪᴘᴘᴇᴅ : <code>{duplicate}</code>\nᴅᴇʟᴇᴛᴇᴅ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ : <code>{deleted}</code>\nɴᴏɴ-ᴍᴇᴅɪᴀ ᴍᴇssᴀɢᴇs sᴋɪᴘᴘᴇᴅ : <code>{no_media + unsupported}</code>\nᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ : <code>{unsupported}</code>\nᴇʀʀᴏʀs ᴏᴄᴄᴜʀʀᴇᴅ : <code>{errors}</code>')
