#use code with proper credit 
# stealing code and mark itas own doesn't make you developer You fool.
#use & customise as per your requirement but with giving proper credit.
#©Rkbotz.t.me ©@infinity_botz.t.me <telegram>
import os, asyncio, requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def upload_image_requests(image_path):
    upload_url = "https://telegra.ph/upload"

    try:
        with open(image_path, 'rb') as file:
            files = {'file': ('file', file, 'image/jpeg')}
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and "src" in result[0]:
                    return "https://graph.org" + result[0]["src"]
                else:
                    raise Exception("ɪɴᴠᴀʟɪᴅ ʀᴇsᴘᴏɴsᴇ ғᴏʀᴍᴀᴛ ғʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴘʜ.")
            else:
                raise Exception(f"ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ ᴡɪᴛʜ sᴛᴀᴛᴜs ᴄᴏᴅᴇ {response.status_code}")
    except Exception as e:
        print(f"ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ᴜᴘʟᴏᴀᴅ : {e}")
        return None
        
@Client.on_message(filters.command("upload") & filters.private)
async def upload_command(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ( ᴘʜᴏᴛᴏ / ᴠɪᴅᴇᴏ ) ᴜɴᴅᴇʀ 5 ᴍʙ")
        return

    if replied.media and hasattr(replied, 'file_size'):
        if replied.file_size > 5242880: #5mb
            await message.reply_text("ғɪʟᴇ sɪᴢᴇ ɪs ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 5 ᴍʙ.")
            return

    infinity_path = await replied.download()

    uploading_message = await message.reply_text("<code>ᴜᴘʟᴏᴀᴅɪɴɢ...</code>")

    try:
        infinity_url = upload_image_requests(infinity_path)
        if not infinity_url:
            raise Exception("ғᴀɪʟᴇᴅ ᴛᴏ ᴜᴘʟᴏᴀᴅ ғɪʟᴇ.")
    except Exception as error:
        await uploading_message.edit_text(f"ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ : {error}")
        return

    try:
        os.remove(infinity_path)
    except Exception as error:
        print(f"ᴇʀʀᴏʀ ʀᴇᴍᴏᴠɪɴɢ ғɪʟᴇ : {error}")
        
    await uploading_message.delete()
    await message.reply_photo(
        photo=f'{infinity_url}',
        caption=f"<b>ʏᴏᴜʀ ᴄʟᴏᴜᴅ ʟɪɴᴋ ᴄᴏᴍᴘʟᴇᴛᴇᴅ 👇</b>\n\nʟɪɴᴋ :-\n\n<code>{infinity_url}</code>",
        #disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(text="• ᴏᴘᴇɴ ʟɪɴᴋ •", url=infinity_url),
            InlineKeyboardButton(text="• sʜᴀʀᴇ ʟɪɴᴋ •", url=f"https://telegram.me/share/url?url={infinity_url}")
        ], [
            InlineKeyboardButton(text="🗑️ ᴄʟᴏsᴇ / ᴅᴇʟᴇᴛᴇ 🗑️", callback_data="close_data")
        ]])
  )

#make you aware again 😏 
# stealing code without credit makes you thief 😂 not developer 
