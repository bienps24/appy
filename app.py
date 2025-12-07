from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ChatMemberHandler
import os
import logging
from time import sleep

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Fetch environment variables (These will be set on Railway or your local environment)
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
VIDEO1_URL = os.getenv('VIDEO1_URL')
VIDEO2_URL = os.getenv('VIDEO2_URL')
VIDEO3_URL = os.getenv('VIDEO3_URL')
BOT_USERNAME = os.getenv('BOT_USERNAME')  # Make sure you set this correctly in the env

# Initialize bot and application
application = Application.builder().token(BOT_API_TOKEN).build()

# Function to send videos privately
async def send_videos(user_id, context):
    try:
        # Delay before sending the videos (5 seconds)
        logger.info("Waiting 5 seconds before sending videos")
        await sleep(5)

        # Send three videos
        logger.info("Sending videos to user: %s", user_id)
        msg1 = await context.bot.send_video(user_id, VIDEO1_URL, caption="Here’s your first video!", disable_notification=True)
        msg2 = await context.bot.send_video(user_id, VIDEO2_URL, caption="Here’s your second video!", disable_notification=True)
        msg3 = await context.bot.send_video(user_id, VIDEO3_URL, caption="Here’s your third video!", disable_notification=True)

        # Wait 30 seconds and delete the videos
        logger.info("Waiting 30 seconds to delete videos")
        await sleep(30)
        await context.bot.delete_message(chat_id=user_id, message_id=msg1.message_id)
        await context.bot.delete_message(chat_id=user_id, message_id=msg2.message_id)
        await context.bot.delete_message(chat_id=user_id, message_id=msg3.message_id)

        # Send reminder after 1 minute
        await sleep(6)  # Wait for another 6 seconds to make it 1 minute from the start
        await context.bot.send_message(
            chat_id=user_id,
            text="Reminder: Don't forget to share for free access or make a payment for global access. Click below to choose your option.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Share 0/2 for Free Access", url="https://t.me/share/url?url=%20Hello%20guys%20Join%20kayo%20FREE%20WATCH%20at%20ACCESS%20https://t.me/joinchat/J7QmfrqcY-U5MTBl")]
            ])
        )
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await context.bot.send_message(chat_id=user_id, text="Sorry, there was an error sending the video.")

# Function to handle when a user starts the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message and provide options in private chat."""
    user = update.message.from_user
    user_id = user.id

    # Send a personal message with buttons
    buttons = [
        [
            InlineKeyboardButton("Share 0/2 for Free Access", url="https://t.me/share/url?url=%20tara%20guys%20sali%20kayo%20𝙡𝙞𝙗𝙧𝙚%20𝙗𝙤𝙨𝙤%20at%20ᴀᴛᴀʙꜱ!%20https://t.me/joinchat/J7QmfrqcY-U5MTBl"),
            InlineKeyboardButton("Don't Want to Share", callback_data="no_share")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=user_id, text="Welcome! Choose an option to join:", reply_markup=reply_markup, disable_notification=True)

    # Call function to send videos and delete them
    await send_videos(user_id, context)

# Handle "Don't Want to Share" option
async def handle_no_share(update, context):
    """Handle the case where the user does not want to share."""
    user = update.callback_query.from_user
    payment_instructions = (
        "To gain **Instant Access** to our **premium content**:\n\n"
        "We offer **Global Access** for only **$20 USD**.\n\n"
        "By purchasing, you will receive access to **9,000 videos** from our extensive collection, available instantly.\n\n"
        "Click the button below to securely proceed with your payment via Telegram's official payment system:\n\n"
    )
    # Add "Proceed with Payment" button below the payment instructions
    payment_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Proceed with Payment", url="https://t.me/Cryptopayphbot?startapp=pay")]
    ])
    
    # Send the payment instructions with the button
    await context.bot.send_message(chat_id=user.id, text=payment_instructions, parse_mode='Markdown', reply_markup=payment_button, disable_notification=True)

# Handle new member joining the group or channel
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a private message to new members when they join the group/channel."""
    for new_user in update.message.new_chat_members:
        logger.info(f"New user joined: {new_user.first_name}")

        # After the new user joins, send them a private message prompting them to interact with the bot
        try:
            # Send a private message to the new user with a link to start the conversation
            await context.bot.send_message(
                chat_id=new_user.id,
                text=f"Hi {new_user.first_name}, welcome! Please start interacting with me by using /start. I'm here to assist you.",
                disable_notification=True
            )

            # Send an invitation link to start a private conversation (with a clickable link)
            invite_link = f"https://t.me/hx7gdusBot?start=start"
            await context.bot.send_message(
                chat_id=new_user.id,
                text=f"Click here to start a private chat with me: {invite_link}",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error sending private message to new user: {e}")

# Handlers
application.add_handler(ChatMemberHandler(new_member))  # Handle new user joining
application.add_handler(CallbackQueryHandler(handle_no_share, pattern="no_share"))
application.add_handler(CommandHandler("start", start))

# Start the bot
application.run_polling()
