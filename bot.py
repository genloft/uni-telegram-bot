
#####################################
# JAGG - 2021                       #
# BOT @universalunibot              #
#####################################
# To deploy to Heroku               #
# ----------------------------------#
# git init                          #
# git add .                         #
# git commit -m "first commit"      #
# heroku git:remote -a your-app     #
# git push heroku master            #
#####################################

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler 
from telegram.utils.helpers import escape_markdown
from telegram.constants import MESSAGEENTITY_MENTION as MENTION

# Import media functions
from media import *

# Import conversation functions
from conversation import *

# Import image recognition
# from imageRecognition import imageDetection, imageDetectionStart

import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
#########################################################
# Please use here your token                            #
# TOKEN = '###########################################' #
#########################################################

# Constants for conversation
SCHOOL, BOOK, BIO = range(3)
# IMAGESENT = range(1)

# Define Menu Options
def cmd_menu_option(update, context):
    query = update.callback_query
    context.user_data['user_id'] = query.message.chat.id
    query.answer()
    choice = query.data

    if choice == "LINKS":
        cmd_links(update, context)
    elif choice == "PHOTO":
        cmd_photo_menu(update, context)
    elif choice == "VIDEO":
        cmd_video(update, context)
    elif choice == "PDF":
        cmd_pdf(update, context)
    elif choice == "LOCATION":
        cmd_location(update, context)
    elif choice == "POLL":
        cmd_poll(update, context)
    elif choice == "PREVIEW":
        cmd_preview(update, context)

    # Add parsing for PHOTOS
    if choice == "PHOTO_1":
        cmd_photo_1(update, context)
    elif choice == "PHOTO_2":
        cmd_photo_2(update, context)

# Define keyboards
def menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Important links", callback_data=str("LINKS"))],
        [InlineKeyboardButton("Check a pic!", callback_data=str("PHOTO"))],
        [InlineKeyboardButton("Check our video!", callback_data=str("VIDEO"))],
        [InlineKeyboardButton("PDf with info", callback_data=str("PDF"))],
        [InlineKeyboardButton("BHSAD location", callback_data=str("LOCATION"))],
        [InlineKeyboardButton("Site URL", callback_data=str("PREVIEW"))],
        [InlineKeyboardButton("Random survey!", callback_data=str("POLL"))]
    ]
    return InlineKeyboardMarkup(keyboard)

# Conversations
basic_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r'\bspeak\b'), conversation)],
    states={
        SCHOOL: [MessageHandler(Filters.regex('^(Product Design|Graphic Design|Illustration|Fashion)$'), school)],
        BOOK: [MessageHandler(Filters.text & ~Filters.command, book)],
        BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# image_conv_handler = ConversationHandler(
#     entry_points=[CommandHandler('image', imageDetectionStart)],
#     states={
#         IMAGESENT: [MessageHandler(Filters.photo & (~Filters.command), imageDetection)],
#     },
#     fallbacks=[CommandHandler('cancel', cancel)],
# )

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.sendSticker(chat_id=update.message.chat.id, sticker="https://pro0.com/stickers/Render6.webp"),
    update.message.reply_text('Hi!, I am Romeo your personal botfriend at BHSAD. If you want me to give some options please type /menu.')

def speak(update, context):
    # Array for multiple answers
    AnswersArray = ["Oh really?. About what?)",
                        "Sure, about what?",
                        "Yes would love to!",
                        "Come on tell me!)",
                        "Perfect let's do that!",
                        "Oh my god was waiting your proposal!",
                        "Yessssssssssssss love to",
                        "Kick it up!",
                        "Shut up!. sure!."]


    # Generate random numb
    randomNumb = getRandomNumber(AnswersArray)

    update.message.reply_text(AnswersArray[randomNumb],
        reply_markup=ReplyKeyboardRemove(),
    )


def help(update, context):
    """Send one message when the command /help is issued."""
    update.message.reply_text("You can check my menu with /menu or start a conversation using / ")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def menu(update, context):
    context.bot.sendSticker(chat_id=update.message.chat.id, sticker="https://pro0.com/stickers/Render13.webp"),
    update.message.reply_text(
        "This is what I can do:",
        reply_markup=menu_keyboard())


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("speak", speak))
    dp.add_handler(basic_conv_handler)
    # dp.add_handler(image_conv_handler)
    dp.add_handler(CallbackQueryHandler(cmd_menu_option))

    # Add handler for group messages
    dp.add_handler(MessageHandler(~Filters.regex(r'\bspeak\b') & Filters.chat_type.groups & Filters.text & ~Filters.entity(MENTION) & ~Filters.command, checkUsernameFromMessage))
    dp.add_handler(MessageHandler(Filters.chat_type.groups & Filters.text & Filters.entity(MENTION) & ~Filters.command, conversationMention))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://uni-bot-juan.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, sincess
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()

    # updater.start_polling()

if __name__ == '__main__':
    main()