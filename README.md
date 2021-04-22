# uni-telegram-bot
A Telegram bot for an University Customer attention and social management
For any issues or support please contact me to info@pro0.com (Juan)

A skeleton and fully functional app with some skills

App is tested and working on Heroku free

HOW TO CUSTOMIZE
1. Place your Telegram token on bot.py that you previously created with Botfather in Telegram
        TOKEN = '######################################'

2. On create_tables.py you should place you credentials on line 16 it is actually configured to work on Heroky postgreSQL services.
        conn = psycopg2.connect(dbname="your-db-name", host="host",
                             user="user", password="pass", sslmode='require')
                             
SOME ACTIONS THAT CAN BE CARRIED OUT

Full media menu
On /menu command you will get a menu with the options to show Links, Photos, Video, PDF, Link preview, a poll or event locations. It is also included submenus that you can test asking for a photo.

Conversational
With any string that contains "speak" word system will start a conversation with you with just 2 steps for now.
You can find logic in bot.py and conversation.py

Social Managing
There is the function conversationMention located on conversation.py that works only if you add the bot to a group.
The system populate a table in postgre with all existing users in the group to ultimately if he does not know the answer will divers to some other random user in the group.

Emotion detection
It has built into the conversation the ability to detect From happyness to angerness and show a different answer for each.

ImageRecognition
On imageRecognition.py you will find the code that locally will work perfectly as it detects the image you are sending. On Heroku free it is not working so use for your development purposes or if you want to upgrade your Heroku account.

Media parsing
Find here all media functions that wotk together with the menu.

Stickers
On bot.py /start command you can find the way to send a Sticker it is stored on my server so you can create your own by converting it to webp
