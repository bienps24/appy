import os
import logging
from time import sleep
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ChatMemberHandler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Fetch environment variables (These will be set on Railway or your local environment)
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')  # API Token from Railway env variables or local setup
ADMIN_ID = os.getenv('ADMIN_ID')  # Admin ID from Railway env variables or local setup

# Initialize bot and application
application = Application.builder().token(BOT_API_TOKEN).build()

# Function to send message with videos and delete them after 30 seconds
async def send_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    # Replace with actual video links
    video1 = "https://raw.githubusercontent.com/biensps24/appy/main/1.mp4"
    video2 = "https://raw.githubusercontent.com/biensps24/appy/main/2.mp4"
    video3 = "https://raw.githubusercontent.com/biensps24/appy/main/3.mp4"

    # Send three videos
    msg1 = await context.bot.send_video(user_id, video1, caption="Here’s your first video!")
    msg2 = await context.bot.send_video(user_id, video2, caption="Here’s your second video!")
    msg3 = await context.bot.send_video(user_id, video3, caption="Here’s your third video!")

    # Wait 30 seconds and delete the videos
    await sleep(30)
    await context.bot.delete_message(chat_id=user_id, message_id=msg1.message_id)
    await context.bot.delete_message(chat_id=user_id, message_id=msg2.message_id)
    await context.bot.delete_message(chat_id=user_id, message_id=msg3.message_id)

    # Send reminder after 1 minute
    await sleep(30)  # Wait for another 30 seconds to make it 1 minute from the start
    await context.bot.send_message(
        chat_id=user_id,
        text="Reminder: Don't forget to share for free access or make a payment for global access. Click below to choose your option.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Share 0/2 for Free Access", url="https://telegram.me/share/url?url=https://t.me/J7QmfrqcY-U5MTBl")],
            [InlineKeyboardButton("Payment Option", url="https://t.me/Cryptopayphbot?startapp=pay")]
        ])
    )

# Function to handle new users and send initial message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message and provide options."""
    user = update.message.from_user
    user_id = user.id

    # Send a personal message with buttons
    buttons = [
        [
            InlineKeyboardButton("Share 0/2 for Free Access", url="https://telegram.me/share/url?url=https://t.me/J7QmfrqcY-U5MTBl"),
            InlineKeyboardButton("Don't Want to Share", callback_data="no_share")
        ],
        [
            InlineKeyboardButton("Payment Option", url="https://t.me/Cryptopayphbot?startapp=pay")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=user_id, text="Welcome! Choose an option to join:", reply_markup=reply_markup)

    # Call function to send videos and delete them
    context.job_queue.run_once(send_videos, 1, context=update)

# Handle "Don't Want to Share" option
async def handle_no_share(update, context):
    """Handle the case where the user does not want to share."""
    user = update.callback_query.from_user
    payment_instructions = (
        "To gain **Instant Access** to our **premium content**:\n\n"
        "We offer **Global Access** for only **$20 USD**.\n\n"
        "By purchasing, you will receive access to **9,000 videos** from our extensive collection, available instantly.\n\n"
        "Click the button below to securely proceed with your payment via Telegram's official payment system:\n\n"
        "[Proceed with Payment](https://t.me/Cryptopayphbot?startapp=pay)"
    )
    await context.bot.send_message(chat_id=user.id, text=payment_instructions, parse_mode='Markdown')

# Handle new member joining the group or channel
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when a new member joins."""
    for new_user in update.message.new_chat_members:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Welcome {new_user.first_name}! I’m your bot. Please check your messages for instructions.")
        await start(update, context)  # Call start method to send the initial message.

# Handlers
application.add_handler(ChatMemberHandler(new_member))  # Correct way to add a ChatMemberHandler
application.add_handler(CallbackQueryHandler(handle_no_share, pattern="no_share"))
application.add_handler(CommandHandler("start", start))

# Start the bot
application.run_polling()
