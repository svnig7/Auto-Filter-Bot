class script(object):
    START_TXT = """<b>ʜᴇʏ {}, <i>{}</i>
    
ɪ ᴀᴍ ᴘᴏᴡᴇʀғᴜʟ ᴀᴜᴛᴏ ғɪʟᴛᴇʀ ᴡɪᴛʜ ʟɪɴᴋ sʜᴏʀᴛᴇɴᴇʀ ʙᴏᴛ.
ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴀꜱ ᴀᴜᴛᴏ ғɪʟᴛᴇʀ ᴡɪᴛʜ ʟɪɴᴋ sʜᴏʀᴛᴇɴᴇʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
ɪᴛ'ꜱ ᴇᴀꜱʏ ᴛᴏ ᴜꜱᴇ ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴀꜱ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇʀᴇ ᴍᴏᴠɪᴇꜱ ᴡɪᴛʜ ʏᴏᴜʀ ʟɪɴᴋ ꜱʜᴏʀᴛᴇɴᴇʀ. ♻️</b>"""

    MY_ABOUT_TXT = """★ sᴇʀᴠᴇʀ : <a href=https://www.heroku.com>ʜᴇʀᴏᴋᴜ</a>
★ ᴅᴀᴛᴀʙᴀsᴇ : <a href=https://www.mongodb.com>ᴍᴏɴɢᴏ ᴅʙ</a>
★ ʟᴀɴɢᴜᴀɢᴇ : <a href=https://www.python.org>ᴘʏᴛʜᴏɴ</a>
★ ʟɪʙʀᴀʀʏ : <a href=https://pyrogram.org>ᴘʀᴏɢʀᴀᴍ</a>"""

    MY_OWNER_TXT = """★ ɴᴀᴍᴇ : sᴠɴ
★ ᴜsᴇʀɴᴀᴍᴇ : @cntct_7bot
★ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ : @imdbposters"""

    STATUS_TXT = """<b>╭━━━━━━━━❰sᴛᴀᴛᴜs ʙᴀʀ❱══❍⊱❁۪۪
┣⪼𖨠 🗃️ ᴛᴏᴛᴀʟ ꜰɪʟᴇs : <code>{}</code>
┣⪼𖨠 👤 ᴛᴏᴛᴀʟ ᴜsᴇʀs : <code>{}</code>
┣⪼𖨠 ♻️ ᴛᴏᴛᴀʟ ᴄʜᴀᴛs : <code>{}</code>
┣⪼𖨠 ✨ ᴜsᴇᴅ sᴛᴏʀᴀɢᴇ : <code>{}</code>
┣⪼𖨠 🆓 ꜰʀᴇᴇ sᴛᴏʀᴀɢᴇ : <code>{}</code>
┣⪼𖨠 🚀 ʙᴏᴛ ᴜᴩᴛɪᴍᴇ : <code>{}</code> 
╰━━━━━━━━━━━━━━━━══❍⊱❁۪۪</b>"""

    NEW_GROUP_TXT = """#NewGroup
ᴛɪᴛʟᴇ - {}
ɪᴅ - <code>{}</code>
ᴜsᴇʀɴᴀᴍᴇ - {}
ᴛᴏᴛᴀʟ - <code>{}</code>"""

    NEW_USER_TXT = """#NewUser
★ ɴᴀᴍᴇ : {}
★ ɪᴅ : <code>{}</code>"""

    NO_RESULT_TXT = """#NoResult
★ ɢʀᴏᴜᴘ ɴᴀᴍᴇ : {}
★ ɢʀᴏᴜᴘ ɪᴅ : <code>{}</code>
★ ɴᴀᴍᴇ : {}

★ ᴍᴇssᴀɢᴇ : {}"""

    REQUEST_TXT = """★ ɴᴀᴍᴇ : {}
★ ɪᴅ : <code>{}</code>

★ ᴍᴇssᴀɢᴇ : {}"""

    NOT_FILE_TXT = """👋 ʜᴇʟʟᴏ {},

ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴇ <b>{}</b> ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ! 🥲

👉 ɢᴏᴏɢʟᴇ sᴇᴀʀᴄʜ ᴀɴᴅ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪs ᴄᴏʀʀᴇᴄᴛ.
👉 ᴘʟᴇᴀsᴇ ʀᴇᴀᴅ ᴛʜᴇ ɪɴsᴛʀᴜᴄᴛɪᴏɴs ᴛᴏ ɢᴇᴛ ʙᴇᴛᴛᴇʀ ʀᴇsᴜʟᴛs.
👉 ᴏʀ ɴᴏᴛ ʙᴇᴇɴ ʀᴇʟᴇᴀsᴇᴅ ʏᴇᴛ."""
    
    EARN_TXT = """<b>ʜᴏᴡ ᴛᴏ ᴇᴀʀɴ ꜰʀᴏᴍ ᴛʜɪs ʙᴏᴛ

➥ ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴇᴀʀɴ ᴍᴏɴᴇʏ ʙʏ ᴜsɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.

» sᴛᴇᴘ 1 :- ғɪʀsᴛ ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴀᴅᴅ ᴛʜɪs ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴ.

» sᴛᴇᴘ 2 :- ᴍᴀᴋᴇ ᴀᴄᴄᴏᴜɴᴛ ᴏɴ <a href=https://onepagelink.in/ref/infinity07>onepagelink.in</a> [ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴜsᴇ ᴏᴛʜᴇʀ sʜᴏʀᴛɴᴇʀ ᴡᴇʙsɪᴛᴇ ]

» sᴛᴇᴘ 3 :- ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ɢɪᴠᴇɴ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ᴡɪᴛʜ ᴛʜɪs ʙᴏᴛ.

➥ ᴛʜɪꜱ ʙᴏᴛ ɪs ꜰʀᴇᴇ ꜰᴏʀ ᴀʟʟ,
ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘs ғᴏʀ ꜰʀᴇᴇ ᴏꜰ ᴄᴏꜱᴛ.</b>"""

    HOW_TXT = """<b>ʜᴏᴡ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ᴏᴡɴ sʜᴏʀᴛɴᴇʀ ‼️

➥ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ᴏᴡɴ sʜᴏʀᴛɴᴇʀ ᴛʜᴇɴ ᴊᴜsᴛ sᴇɴᴅ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴇᴛᴀɪʟs ɪɴ ᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ

➥ ғᴏʀᴍᴀᴛ ↓↓↓

<code>/set_shortlink sʜᴏʀᴛɴᴇʀ sɪᴛᴇ sʜᴏʀᴛɴᴇʀ ᴀᴘɪ</code>

➥ ᴇxᴀᴍᴘʟᴇ ↓↓↓

<code>/set_shortlink onepagelink.in f646357aa129cfbd7eb59bcba428096ab54ca950</code>

➥ ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜɪᴄʜ sʜᴏʀᴛᴇɴᴇʀ ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛʜᴇɴ sᴇɴᴅ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ /get_shortlink

📝 ɴᴏᴛᴇ :- ʏᴏᴜ sʜᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ɪɴ ɢʀᴏᴜᴘ. sᴇɴᴅ ᴄᴏᴍᴍᴀɴᴅ ᴡɪᴛʜᴏᴜᴛ ʙᴇɪɴɢ ᴀɴ ᴀɴᴏɴʏᴍᴜs ᴀᴅᴍɪɴ.</b>"""

    IMDB_TEMPLATE = """✅ ɪ ғᴏᴜɴᴅ : <code>{query}</code>

🏷 ᴛɪᴛʟᴇ : <a href={url}>{title}</a>
🎭 ɢᴇɴʀᴇs : {genres}
📆 ʏᴇᴀʀ : <a href={url}/releaseinfo>{year}</a>
🌟 ʀᴀᴛɪɴɢ : <a href={url}/ratings>{rating} / 10</a>
☀️ ʟᴀɴɢᴜᴀɢᴇs : {languages}
📀 ʀᴜɴᴛɪᴍᴇ : {runtime} ᴍɪɴᴜᴛᴇs

🗣 ʀᴇᴏ̨ᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}
©️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : <b>{message.chat.title}</b>"""

    FILE_CAPTION = """<i>{file_name}</i>

🚫 ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴄʟᴏsᴇ ʙᴜᴛᴛᴏɴ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ sᴇᴇɴ ᴛʜᴇ ᴍᴏᴠɪᴇ 🚫"""

    WELCOME_TEXT = """👋 ʜᴇʟʟᴏ {mention},
    ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {title} ɢʀᴏᴜᴘ ! 💞"""

    HELP_TXT = """<b>ɴᴏᴛᴇ - <spoiler>ᴛʀʏ ᴇᴀᴄʜ ᴄᴏᴍᴍᴀɴᴅ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴀʀɢᴜᴍᴇɴᴛ ᴛᴏ sᴇᴇ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs 😹</spoiler></b>"""
    
    ADMIN_COMMAND_TXT = """<b>ʜᴇʀᴇ ɪs ʙᴏᴛ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs 👇

/index_channels - to check how many index channel id added
/stats - to get bot status
/delete - to delete files using query
/delete_all - to delete all indexed file
/broadcast - to send message to all bot users
/grp_broadcast - to send message to all groups
/pin_broadcast - to send message as pin to all bot users.
/pin_grp_broadcast - to send message as pin to all groups.
/restart - to restart bot
/speedtest - check ul/dl
/leave - to leave your bot from particular group
/unban_grp - to enable group
/ban_grp - to disable group
/ban_user - to ban a users from bot
/unban_user - to unban a users from bot
/users - to get all users details
/chats - to get all groups
/invite_link - to generate invite link
/index - to index bot accessible channels
/add_premium - to add user in premium
/remove_premium - to remove user from premium</b>"""

    GROUP_COMMAND_TXT = """<b>ʜᴇʀᴇ ɪs sᴏᴍᴇ (ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ) ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs
/manage - To perform bulk group actions
/ban - To ban a member from group
/unban - To unban a member from group
/mute - To mute a member from group
/unmute - To unmute a member from group
/settings - to change group settings as your wish
/set_template - to set custom imdb template
/set_caption - to set custom bot files caption
/set_shortlink - group admin can set custom shortlink
/get_custom_settings - to get your group settings details
/set_welcome - to set custom new joined users welcome message for group
/set_tutorial - to set custom tutorial link in result page button
/id - to check group or channel id

    ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴀᴛ ʙᴏᴛ ʜᴀs ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀs ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ.</b>"""
    
    USER_COMMAND_TXT = """<b>ʜᴇʀᴇ ɪs ʙᴏᴛ ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs 👇

/start - to check bot alive or not
/settings - to change group settings as your wish
/set_template - to set custom imdb template
/set_caption - to set custom bot files caption
/set_shortlink - group admin can set custom shortlink
/get_custom_settings - to get your group settings details
/set_welcome - to set custom new joined users welcome message for group
/set_tutorial - to set custom tutorial link in result page button
/id - to check group or channel id
/my_plan - to check your plan details
/plans - to get plan details</b>"""

    SOURCE_TXT = """<b>ʙᴏᴛ ɢɪᴛʜᴜʙ ʀᴇᴘᴏsɪᴛᴏʀʏ -

- ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ᴀɴ ᴏᴘᴇɴ ꜱᴏᴜʀᴄᴇ ᴘʀᴏᴊᴇᴄᴛ.

- ꜱᴏᴜʀᴄᴇ - <a href=https://github.com/GRVGK7/Auto-Filter-Bot>ʜᴇʀᴇ</a>

- ᴅᴇᴠʟᴏᴘᴇʀ - @svntg7"""
