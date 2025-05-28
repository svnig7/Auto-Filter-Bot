# © Rkbotz.t.me | @infinity_botz.t.me | Give credit if you use it

import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def upload_image_to_telegra_ph(image_path: str) -> str | None:
    """Uploads an image to telegra.ph and returns the image URL."""
    try:
        with open(image_path, "rb") as f:
            files = {'file': ('file', f, 'image/jpeg')}
            response = requests.post("https://telegra.ph/upload", files=files)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and "src" in result[0]:
                return f"https://graph.org{result[0]['src']}"
            raise Exception("Invalid response from Telegraph.")
        else:
            raise Exception(f"Upload failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error during upload: {e}")
        return None

@Client.on_message(filters.command("upload") & filters.private)
async def handle_upload(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("Please reply to a **photo** (under 5 MB) to upload.")
        return

    # Check size and file type
    if not (replied.photo or (replied.document and replied.document.mime_type.startswith("image/"))):
        await message.reply_text("Only image files (photo/doc) are supported.")
        return

    if hasattr(replied, "file_size") and replied.file_size > 5 * 1024 * 1024:
        await message.reply_text("Image size exceeds 5MB limit.")
        return

    uploading_msg = await message.reply_text("<code>Uploading to Telegraph...</code>")
    file_path = await replied.download()

    try:
        url = upload_image_to_telegra_ph(file_path)
        if not url:
            raise Exception("Upload failed.")
    except Exception as err:
        await uploading_msg.edit_text(f"❌ Failed to upload: <code>{err}</code>")
        return
    finally:
        try:
            os.remove(file_path)
        except Exception as cleanup_error:
            print(f"Cleanup failed: {cleanup_error}")

    await uploading_msg.delete()
    await message.reply_photo(
        photo=url,
        caption=f"<b>✅ Uploaded Successfully!</b>\n\n🔗 Link:\n<code>{url}</code>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• Open Link •", url=url)],
            [InlineKeyboardButton("• Share •", url=f"https://t.me/share/url?url={url}")],
            [InlineKeyboardButton("🗑️ Delete", callback_data="close_data")]
        ])
        )
