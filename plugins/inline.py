import logging, time
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQuery
from database.ia_filterdb import get_search_results
from database.users_chats_db import db
from utils import is_subscribed, get_size, temp, get_verify_status, update_verify_status
from info import CACHE_TIME, AUTH_CHANNEL, SUPPORT_LINK, UPDATES_LINK, FILE_CAPTION, IS_VERIFY, VERIFY_EXPIRE

cache_time = 0 if AUTH_CHANNEL else CACHE_TIME

def is_banned(query: InlineQuery):
    return query.from_user and query.from_user.id in temp.BANNED_USERS

@Client.on_inline_query()
async def inline_search(bot, query):
    """sʜᴏᴡ sᴇᴀʀᴄʜ ʀᴇsᴜʟᴛs ғᴏʀ ɢɪᴠᴇɴ ɪɴʟɪɴᴇ ᴏ̨ᴜᴇʀʏ"""

    if is_banned(query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text="ʏᴏᴜ'ʀᴇ ʙᴀɴɴᴇᴅ ᴜsᴇʀ :(",
                           switch_pm_parameter="start")
        return


    results = []
    string = query.query
    offset = int(query.offset or 0)
    files, next_offset, total = await get_search_results(string, offset=offset)

    for file in files:
        reply_markup = get_reply_markup()
        f_caption=FILE_CAPTION.format(
            caption=file.caption,
            file_size=get_size(file.file_size)
        )
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                document_file_id=file.file_id,
                caption=f_caption,
                description=f'Size: {get_size(file.file_size)}',
                reply_markup=reply_markup))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} ʀᴇsᴜʟᴛs - {total}"
        if string:
            switch_pm_text += f' ғᴏʀ : {string}'
        await query.answer(results=results,
                        is_personal = True,
                        cache_time=cache_time,
                        switch_pm_text=switch_pm_text,
                        switch_pm_parameter="start",
                        next_offset=str(next_offset))
    else:
        switch_pm_text = f'{emoji.CROSS_MARK} ɴᴏ ʀᴇsᴜʟᴛs'
        if string:
            switch_pm_text += f' ғᴏʀ : {string}'
        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start")


def get_reply_markup():
    buttons = [[
        InlineKeyboardButton('⚡️ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ⚡️', url=UPDATES_LINK),
        InlineKeyboardButton('💡 ʀᴇᴏ̨ᴜᴇsᴛ ɢʀᴏᴜᴘ 💡', url=SUPPORT_LINK)
    ]]
    return InlineKeyboardMarkup(buttons)
