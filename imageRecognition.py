from telegram import Update
from telegram.ext import CallbackContext

import os

# Import YOLO model
from sightseer import Sightseer
from sightseer.zoo import YOLOv3Client

# Constants for conversation
IMAGESENT = range(1)

def imageDetectionStart(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please send an image file in order for me to detect the objects inside it\n'
        'Send /cancel to stop talking to me.\n\n')

    return IMAGESENT

def imageDetection(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait while I analyze the Image.")
    downloaded_path = "img"
    file_id = update.message.photo[-1].file_id
    file_unique_id = update.message.photo[-1].file_unique_id

    new_file= context.bot.get_file(file_id)
    saving_path= os.path.join(downloaded_path, "{}.jpg".format(file_unique_id))
    new_file.download(saving_path)

    yolo = YOLOv3Client()
    yolo.load_model() # downloads weights

    # loading image from local system
    ss = Sightseer()
    image = ss.load_image(saving_path)
    
    preds, pred_img = yolo.predict(image, return_img=True)

    itemsStrings = "It seems to me that this image contains:\n"
    for items in preds:
        itemsStrings += str(items[0]) + "\n"
        break

    context.bot.send_message(chat_id=update.effective_chat.id, text=itemsStrings)