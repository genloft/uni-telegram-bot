from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,)

# Random
import random

# Text 2 Emotion
import text2emotion as te

# Import DB Handler
import psycopg2

# Constants for conversation
SCHOOL, BOOK, BIO = range(3)

# Array for multiple answers
bookAnswersArray = ["I see! Please tell me your best book title,\nso I know what you like!",
                    "Do you like books? What are you reading now?",
                    "Which book did you like most?"]

bioAnswersArray = ["At last, tell me something about yourself.",
                    "You seem an interesting person, tell me more about yourself!",
                    "You are interesting, tell me more about you!"]

# Get random number
def getRandomNumber(array):
    length = len(array)
    return random.randint(0, length - 1)

# Start conversation
def conversation(update: Update, context: CallbackContext) -> int:
    # Initialize the school name keyboard
    reply_keyboard = [['Product Design', 'Graphic Design', 'Illustration', 'Fashion']]

    context.bot.sendSticker(chat_id=update.message.chat.id, sticker="https://pro0.com/stickers/Render9.webp")

    update.message.reply_text(
        'Hi! My name is Conversation Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Which school are you from?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return SCHOOL

def school(update: Update, context: CallbackContext) -> int:
    # Save school answer
    context.user_data['school'] = update.message.text

    # Generate random numb
    randomNumb = getRandomNumber(bookAnswersArray)

    update.message.reply_text(bookAnswersArray[randomNumb],
        reply_markup=ReplyKeyboardRemove(),
    )

    return BOOK

def book(update: Update, context: CallbackContext) -> int:
    # Save book answer
    context.user_data['book'] = update.message.text

    # Generate random numb
    randomNumb = getRandomNumber(bioAnswersArray)

    update.message.reply_text(bioAnswersArray[randomNumb])

    return BIO

def bio(update: Update, context: CallbackContext) -> int:
    # Save bio answer
    context.user_data['bio'] = update.message.text
    
    # Get chat ID
    chatID = update.message.chat.id

    # Concat book answer
    # userAnswers = context.user_data['book']

    # Get the emotion and print in console
    userEmotion = te.get_emotion(update.message.text)

    # Set emotions text
    emotionText = None
    if userEmotion['Happy'] >= 0.5:
        emotionText = "I see that you are happy today!"
    elif userEmotion['Sad'] >= 0.5:
        emotionText = "I see that you are sad today, how can I help?"
    elif userEmotion['Angry'] >= 0.5:
        emotionText = "I see that you are a bit angry today, how can I help?"

    if emotionText:
        context.bot.send_message(chat_id=chatID,
                                text=emotionText)

    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END

# Conversation Functions
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

# Check DB for users
def checkUsers(username):
    """ Check if user is in the users table """
    sqlCheck = """SELECT * FROM users
             WHERE user_name = %s;"""

    """ insert a new user into the users table """
    sqlInsert = """INSERT INTO users(user_name)
             VALUES(%s)"""

    try:
        # Connect to postgres table
        conn = psycopg2.connect(dbname="d9p0qicl7pm3vq", host="ec2-176-34-222-188.eu-west-1.compute.amazonaws.com",
                        user="lokvtsuxecycfi", password="bf7217b8d02ceac97a86dd48d5f6a3d3e68fceb7917f22e82eb422157b240a90", sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sqlCheck, (username, ))
        # get the return from select statement
        userInDB = cur.fetchall()
        # Add the user if it does not exist
        if not userInDB:
            # create a new cursor
            cur2 = conn.cursor()
            cur2.execute(sqlInsert, (username, ))
            # Commit the changes to the database
            conn.commit()
            cur2.close()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# Check username from group message
def checkUsernameFromMessage(update, context):
    username = str(update.message.from_user.username)
    checkUsers(username)

# Get random user from DB
def getRandomUserfromDB():
    """ Get user from the users table """
    sqlCount = """SELECT COUNT(*) FROM users"""
    """ Get user from the users table """
    sqlGet = """SELECT user_name FROM users
             OFFSET floor(random()*%s) LIMIT 1;"""

    try:
        # Connect to postgres table
        conn = psycopg2.connect(dbname="d9p0qicl7pm3vq", host="ec2-176-34-222-188.eu-west-1.compute.amazonaws.com",
                        user="lokvtsuxecycfi", password="bf7217b8d02ceac97a86dd48d5f6a3d3e68fceb7917f22e82eb422157b240a90", sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sqlCount)
        # get the return from select statement
        nbUserInDB = cur.fetchall()
        nbUserInDB = int(nbUserInDB[0][0])

        # Check if DB is empty
        if nbUserInDB <= 0:
            return None

        # Get random user
        # create a new cursor
        cur2 = conn.cursor()
        cur2.execute(sqlGet, (nbUserInDB, ))
        # get the return from select statement
        getUsername = cur2.fetchone()
        cur2.close()
        # Close communication with the PostgreSQL database
        cur.close()
        return getUsername[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# Conversation Mention
def conversationMention(update, context):
    username = getRandomUserfromDB()
    username = '@' + str(username)
    if username:
        update.message.reply_text('I cannot help you with this question, maybe {}'.format(username))
    else:
        update.message.reply_text('I cannot help you with this question, maybe an admin can')