from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image
import requests, os

def convert_to_jpeg(image_path):
    new_path = image_path.rsplit('.', 1)[0] + ".jpg"
    try:
        img = Image.open(image_path).convert("RGB")
        img.save(new_path, "JPEG")
        return new_path
    except Exception as e:
        print(f"Conversion error: {e}")
        return None

def upload_to_telegra_ph(image_path):
    try:
        with open(image_path, 'rb') as f:
            response = requests.post("https://telegra.ph/upload", files={"file": ("file", f, "image/jpeg")})
            if response.status_code == 200:
                return "https://graph.org" + response.json()[0]["src"]
            else:
                raise Exception(f"Upload failed with status code {response.status_code}")
    except Exception as e:
        raise Exception(f"Upload failed: {e}")

@Client.on_message(filters.command("upload") & filters.private)
async def upload_handler(client, message):
    replied = message.reply_to_message
    if not replied or not (replied.photo or replied.document):
        await message.reply_text("📸 Reply to a photo or image file (under 5MB) to upload.")
        return

    # Check file size
    if hasattr(replied, 'file_size') and replied.file_size > 5242880:
        await message.reply_text("⚠️ File size is too large. Please upload files under 5MB.")
        return

    temp_path = await replied.download()
    jpeg_path = convert_to_jpeg(temp_path)
    if not jpeg_path:
        await message.reply_text("❌ Failed to convert image to JPEG.")
        return

    uploading_msg = await message.reply_text("📤 Uploading to Telegra.ph...")

    try:
        telegraph_url = upload_to_telegra_ph(jpeg_path)
    except Exception as e:
        await uploading_msg.edit(f"❌ Failed to upload: <code>{e}</code>")
        return
    finally:
        try:
            os.remove(temp_path)
            if jpeg_path != temp_path:
                os.remove(jpeg_path)
        except:
            pass

    await uploading_msg.delete()
    await message.reply_photo(
        photo=telegraph_url,
        caption=f"<b>✅ Your image link is ready:</b>\n<code>{telegraph_url}</code>",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🌐 Open Link", url=telegraph_url),
            InlineKeyboardButton("🔗 Share Link", url=f"https://t.me/share/url?url={telegraph_url}")
        ], [
            InlineKeyboardButton("🗑️ Delete", callback_data="close_data")
        ]])
    )
