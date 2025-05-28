import os
from info import ADMINS
from speedtest import Speedtest, ConfigRetrievalError
from pyrogram import Client, filters, enums
from utils import get_size
from datetime import datetime
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
import logging


@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text(f'★ ᴜsᴇʀ ɪᴅ : <code>{message.from_user.id}</code>')

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.reply_text(f'★ ɢʀᴏᴜᴘ ɪᴅ : <code>{message.chat.id}</code>')

    elif chat_type == enums.ChatType.CHANNEL:
        await message.reply_text(f'★ ᴄʜᴀɴɴᴇʟ ɪᴅ : <code>{message.chat.id}</code>')

@Client.on_message(filters.command('speedtest') & filters.user(ADMINS))
async def speedtest(client, message):
    #from - https://github.com/weebzone/WZML-X/blob/master/bot/modules/speedtest.py
    msg = await message.reply_text("ɪɴɪᴛɪᴀᴛɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ...")
    try:
        speed = Speedtest()
    except ConfigRetrievalError:
        await msg.edit("ᴄᴀɴ'ᴛ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ sᴇʀᴠᴇʀ ᴀᴛ ᴛʜᴇ ᴍᴏᴍᴇɴᴛ, ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ !")
        return
    speed.get_best_server()
    speed.download()
    speed.upload()
    speed.results.share()
    result = speed.results.dict()
    photo = result['share']
    text = f'''
➲ <b>sᴘᴇᴇᴅᴛᴇsᴛ ɪɴғᴏ</b>
┠ <b>ᴜᴘʟᴏᴀᴅ :</b> <code>{get_size(result['upload'])}/s</code>
┠ <b>ᴅᴏᴡɴʟᴏᴀᴅ :</b>  <code>{get_size(result['download'])}/s</code>
┠ <b>ᴘɪɴɢ :</b> <code>{result['ping']} ms</code>
┠ <b>ᴛɪᴍᴇ :</b> <code>{datetime.strptime(result['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")}</code>
┠ <b>ᴅᴀᴛᴀ sᴇɴᴛ :</b> <code>{get_size(int(result['bytes_sent']))}</code>
┖ <b>ᴅᴀᴛᴀ ʀᴇᴄᴇɪᴠᴇᴅ :</b> <code>{get_size(int(result['bytes_received']))}</code>

➲ <b>sᴘᴇᴇᴅᴛᴇsᴛ sᴇʀᴠᴇʀ</b>
┠ <b>ɴᴀᴍᴇ :</b> <code>{result['server']['name']}</code>
┠ <b>ᴄᴏᴜɴᴛʀʏ :</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
┠ <b>sᴘᴏɴsᴏʀ :</b> <code>{result['server']['sponsor']}</code>
┠ <b>ʟᴀᴛᴇɴᴄʏ :</b> <code>{result['server']['latency']}</code>
┠ <b>ʟᴀᴛɪᴛᴜᴅᴇ :</b> <code>{result['server']['lat']}</code>
┖ <b>ʟᴏɴɢɪᴛᴜᴅᴇ :</b> <code>{result['server']['lon']}</code>

➲ <b>ᴄʟɪᴇɴᴛ ᴅᴇᴛᴀɪʟs</b>
┠ <b>ɪᴘ ᴀᴅᴅʀᴇss :</b> <code>{result['client']['ip']}</code>
┠ <b>ʟᴀᴛɪᴛᴜᴅᴇ :</b> <code>{result['client']['lat']}</code>
┠ <b>ʟᴏɴɢɪᴛᴜᴅᴇ :</b> <code>{result['client']['lon']}</code>
┠ <b>ᴄᴏᴜɴᴛʀʏ :</b> <code>{result['client']['country']}</code>
┠ <b>ɪsᴘ :</b> <code>{result['client']['isp']}</code>
┖ <b>ɪsᴘ ʀᴀᴛɪɴɢ :</b> <code>{result['client']['isprating']}</code>
'''
    await message.reply_photo(photo=photo, caption=text)
    await msg.delete()
