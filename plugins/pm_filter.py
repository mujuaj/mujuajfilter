#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**✪ ഫയലുകൾ ലഭിക്കുന്നതിനായി നിങ്ങൾ ഞങ്ങളുടെ 𝗠𝗔𝗜𝗡 ചാനലിൽ 𝗝𝗢𝗜𝗡 ചെയ്യണം😁😁ചാനലിൽ ജോയിൻ ആയ ശേഷം\n  ▏↩️ 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡 ▏\n ബട്ടൺ ക്ലിക്ക് ചെയ്യുക\n\n✪ ✪ 𝗬𝗼𝘂 𝗡𝗲𝗲𝗱 𝗧𝗼 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗔𝗜𝗡 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗮𝗻𝗱 𝗣𝗿𝗲𝘀𝘀\n ▏↩️ 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡 ▏\n𝗕𝘂𝘁𝘁𝗼𝗻 𝘁𝗼 𝗴𝗲𝘁 𝘁𝗵𝗲 𝗙𝗶𝗹𝗲.**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 𝗝𝗢𝗜𝗡 𝗠𝗔𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADMwIAAtbcmFelnLaGAZhgBwI')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None 
            buttons = [[InlineKeyboardButton("🔲 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🔲", url="https://t.me/AJmovieLINKS")]]  + buttons
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\nപടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇  ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n 𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\nപടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇 ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text=" ☄ 𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 📇",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔖 𝗣𝗮𝗴𝗲 1/{data['total']}",callback_data="pages")]
        )
        poster=None 
        buttons = [[InlineKeyboardButton("🔲 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🔲", url="https://t.me/AJmovieLINKS")]]  + buttons
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\nപടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇 ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n 𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\nപടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇 ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"🎪 [{get_size(file.file_size)}] 🚀{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🔖𝗣𝗔𝗚𝗘𝗦 1/1",callback_data="pages")]
            )
            poster=None 
            buttons = [[InlineKeyboardButton("🔲 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🔲", url="https://t.me/AJmovieLINKS")]]  + buttons
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\nപടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n 𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\nപടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇 ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="☄ 𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 📇",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔖 𝗣𝗮𝗴𝗲 1/{data['total']}",callback_data="pages")]
        )
        poster=None 
        buttons = [[InlineKeyboardButton("🔲 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🔲", url="https://t.me/AJmovieLINKS")]]  + buttons
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n 𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\nപടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇 ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>🎬𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬:{search}\n\n𝐅𝐑𝐎𝐌:◻⬜@AJmovieLINKS⬛◼\n\n𝗣𝗿𝗲𝘀𝘀 𝗧𝗵𝗲 𝗗𝗼𝘄𝗻 𝗕𝘂𝘁𝘁𝗼𝗻𝘀 \nＡＮＤ ＣＬＩＣＫ ＳＴＡＲＴ\n𝗧𝗼 𝗔𝗰𝗰𝗲𝘀𝘀 𝗧𝗵𝗲 𝗙𝗶𝗹𝗲\n പടം ലഭിക്കുന്നതിനായി താഴെ കാണുന്ന ബട്ടണുകളിൽ ക്ലിക്ക് ചെയ്യുക👇 ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ 𝘽𝙖𝙘𝙠", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"┏༼ ◉ ╭╮ ◉༽┓  🔖 𝗣𝗮𝗴𝗲 {int(index)+2}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ 𝘽𝙖𝙘𝙠", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("𝙉𝙚𝙭𝙩 ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"┏༼ ◉ ╭╮ ◉༽┓  🔖 𝗣𝗮𝗴𝗲 {int(index)+2}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("☄ 𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 📇", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"┏༼ ◉ ╭╮ ◉༽┓  🔖 𝗣𝗮𝗴𝗲 {int(index)}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ 𝘽𝙖𝙘𝙠", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("𝙉𝙚𝙭𝙩 ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"┏༼ ◉ ╭╮ ◉༽┓  🔖 𝗣𝗮𝗴𝗲 {int(index)}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('║𝗨𝗽𝗱𝗮𝘁𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹║', url='https://t.me/worldmoviesaj'),
                    InlineKeyboardButton('╽𝗠𝗼𝗿𝗲 𝗠𝗼𝘃𝗶𝗲𝘀╽', url='https://t.me/worldmoviesaj')
                ]
                ]
            await query.message.edit(text="<b>Developer : <a href='https://t.me/avataradorn'>AJ</a>\nLanguage : <code>Python3</code>\nLibrary : <a href='https://t.me/worldmoviesaj/'>Pyrogram asyncio</a>\nSource Code : <a href='https://t.me/AJmovieLINKS'>Click here</a>\nUpdate Channel : <a href='https://t.me/worldmoviesaj'>AJ Bots</a> </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)



        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('╽𝗠𝗼𝗿𝗲 𝗠𝗼𝘃𝗶𝗲𝘀╽', url='https://t.me/worldmoviesaj'),
                        InlineKeyboardButton('║𝗨𝗽𝗱𝗮𝘁𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹║', url='https://t.me/worldmoviesaj')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("𝐀𝐅𝐓𝐄𝐑 𝐉𝐎𝐈𝐍𝐈𝐍𝐆 𝐌𝐀𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐂𝐋𝐈𝐂𝐊 𝐌𝐄 ,𝐀𝐍𝐃 𝐘𝐎𝐔 𝐖𝐈𝐋𝐋 𝐆𝐄𝐓 𝐓𝐇𝐄 𝐅𝐈𝐋𝐄☺️",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('╽𝗠𝗼𝗿𝗲 𝗠𝗼𝘃𝗶𝗲𝘀╽', url='https://t.me/worldmoviesaj'),
                        InlineKeyboardButton('║𝗨𝗽𝗱𝗮𝘁𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹║', url='https://t.me/worldmoviesaj')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("𝙄𝙏𝙎 𝙏𝙃𝙀 𝙍𝙀𝙌𝙐𝙀𝙎𝙏 𝙊𝙁 𝘼𝙉𝙊𝙏𝙃𝙀𝙍 𝙋𝙀𝙍𝙎𝙊𝙉 😅🙃𝙏𝙊 𝙂𝙊 𝙏𝙊 𝙉𝙀𝙓𝙏 𝙋𝘼𝙂𝙀,𝙔𝙊𝙐 𝙍𝙀𝙌𝙐𝙀𝙎𝙏 𝙄𝙉 𝘾𝙃𝘼𝙏 𝘼𝙉𝘿 𝘾𝙇𝙄𝘾𝙆  ╽ 𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 📇 ╽ 𝘽𝙐𝙏𝙏𝙊𝙉 😁",show_alert=True)
