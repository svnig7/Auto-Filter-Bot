from pyrogram import Client, filters, enums
from utils import is_check_admin
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command('manage') & filters.group)
async def members_management(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
  btn = [[
    InlineKeyboardButton('ᴜɴᴍᴜᴛᴇ ᴀʟʟ', callback_data=f'unmute_all_members'),
    InlineKeyboardButton('ᴜɴʙᴀɴ ᴀʟʟ', callback_data=f'unban_all_members')
  ],[
    InlineKeyboardButton('ᴋɪᴄᴋ ᴍᴜᴛᴇᴅ ᴜsᴇʀs', callback_data=f'kick_muted_members'),
    InlineKeyboardButton('ᴋɪᴄᴋ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs', callback_data=f'kick_deleted_accounts_members')
  ]]
  await message.reply_text("sᴇʟᴇᴄᴛ ᴏɴᴇ ᴏғ ғᴜɴᴄᴛɪᴏɴ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴍᴇᴍʙᴇʀs.", reply_markup=InlineKeyboardMarkup(btn))
  
  
@Client.on_message(filters.command('ban') & filters.group)
async def ban_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴜsᴇʀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀ ɪᴅ, ᴜsᴇʀɴᴀᴍᴇ")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("ᴄᴀɴ'ᴛ ғɪɴᴅ ʏᴏᴜʀ ɢɪᴠᴇɴ ᴜsᴇʀ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
  try:
    await client.ban_chat_member(message.from_user.id, user_id)
  except:
    return await message.reply_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ʙᴀɴ ᴜsᴇʀ")
  await message.reply_text(f'sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ {user.mention} ғʀᴏᴍ {message.chat.title}')


@Client.on_message(filters.command('mute') & filters.group)
async def mute_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴜsᴇʀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀ ɪᴅ, ᴜsᴇʀɴᴀᴍᴇ")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("ᴄᴀɴ'ᴛ ғɪɴᴅ ʏᴏᴜʀ ɢɪᴠᴇɴ ᴜsᴇʀ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
  try:
    await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
  except:
    return await message.reply_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴍᴜᴛᴇ ᴜsᴇʀ")
  await message.reply_text(f'sᴜᴄᴄᴇssғᴜʟʟʏ ᴍᴜᴛᴇᴅ {user.mention} ғʀᴏᴍ {message.chat.title}')


@Client.on_message(filters.command(["unban", "unmute"]) & filters.group)
async def unban_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.')
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴜsᴇʀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀ ɪᴅ, ᴜsᴇʀɴᴀᴍᴇ")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("ᴄᴀɴ'ᴛ ғɪɴᴅ ʏᴏᴜʀ ɢɪᴠᴇɴ ᴜsᴇʀ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ")
  try:
    await client.unban_chat_member(message.chat.id, user_id)
  except:
    return await message.reply_text(f"ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ {message.command[0]} ᴜsᴇʀ")
  await message.reply_text(f'sᴜᴄᴄᴇssғᴜʟʟʏ {message.command[0]} {user.mention} ғʀᴏᴍ {message.chat.title}')
