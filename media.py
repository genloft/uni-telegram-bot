# media.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Location

# Define keyboard
# Links Keyboard
def links_keyboard():
    keyboard = [
        [InlineKeyboardButton("Courses", url="https://britishdesign.ru/en/courses")],
        [InlineKeyboardButton("About", url="https://britishdesign.ru/en/about")],
        [InlineKeyboardButton("Career", url="https://britishdesign.ru/en/career")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Photo Keyboard
def photo_keyboard():
    keyboard = [
        [InlineKeyboardButton("Fashion", callback_data=str("PHOTO_1"))],
        [InlineKeyboardButton("Product Design", callback_data=str("PHOTO_2"))],
    ]
    return InlineKeyboardMarkup(keyboard)

# Links
def cmd_links(update, context):
    context.bot.send_message(chat_id=context.user_data['user_id'],text="Links:",
    reply_markup=links_keyboard())

# Video
def cmd_video(update, context):
    # We can send mp4 videos this way.
    # video_url = "Video_url"
    # context.bot.send_video(chat_id=context.user_data['user_id'], video=video_url, supports_streaming=True)

    # YT Video can be autoplayed in telegram, we can send normal message
    context.bot.send_message(chat_id=context.user_data['user_id'], disable_web_page_preview=False,
    text="""{VIDEO}""".format(VIDEO="https://youtu.be/hAjTxrq78U4"))

# Photos
def cmd_photo_1(update, context):
    context.bot.send_photo(chat_id=context.user_data['user_id'], photo="https://britishdesign.ru/upload/resize_cache/iblock/d91/1160_520_1/5cddecabb0027f7ed3bc965780e79663.jpg", 
    caption="""This is a photo caption 1""")

def cmd_photo_2(update, context):
    context.bot.send_photo(chat_id=context.user_data['user_id'], photo="https://britishdesign.ru/upload/resize_cache/iblock/471/1160_520_1/47162405b7aaca09e0deb682bd998e51.jpg", 
    caption="""This is a photo caption 2""")

# Photo Menu
def cmd_photo_menu(update, context):
    context.bot.send_message(chat_id=context.user_data['user_id'],text="Photos:",
    reply_markup=photo_keyboard())

# PDF
def cmd_pdf(update, context):
    context.bot.send_document(chat_id=context.user_data['user_id'], document="https://britishdesign.ru/courses/Programme_Specification_BA_(HONS)_IAD.pdf")

# Location
def cmd_location(update, context):
    uni_location = Location(55.752117352461404, 37.6696309153444)
    context.bot.send_location(chat_id=context.user_data['user_id'], location=uni_location)

# Poll
def cmd_poll(update, context):
    context.bot.send_poll(chat_id=context.user_data['user_id'], question="Are you comfortable speaking with me?:", options=["Yes","No","Not sure","Totally!","Nevermore!"])

# Link Preview
def cmd_preview(update, context):
    context.bot.send_message(chat_id=context.user_data['user_id'], disable_web_page_preview=False,
    text="""Link Preview: {LINK}""".format(LINK="https://britishdesign.ru/en/work-at-bhsad/"))