import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatMemberUpdated
from aiogram.utils.exceptions import BadRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
API_TOKEN = "7667485425:AAHEQnW7MHgA3VkiPqRSSlv3dotQ8slT2ZY"
OWNER_ID = 7856842830 # Replace with your Telegram user ID

db = {"sudo_users": []}  # Temporary in-memory database for sudo users

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Send a welcome message."""
    await message.reply(
        "Hello! I'm Edit Guardian Bot. Here's what I can do:\n"
        "1. Notify about edited messages.\n"
        "2. Detect deleted messages (if permissions allow).\n"
        "3. Log all messages for analysis.\n"
        "4. Respond to specific keywords.\n"
        "5. Manage admin-related events.\n"
        "6. Retrieve user info.\n"
        "7. Broadcast messages to all members.\n"
        "8. Manage sudo users.\n"
        "Use /settings to configure me!"
    )

@dp.message_handler(commands=['addsudo'])
async def add_sudo_user(message: types.Message):
    """Add a sudo user. Only the owner can use this command."""
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    # Extract user ID to add from the command arguments
    try:
        args = message.text.split()
        user_id = int(args[1])
    except (IndexError, ValueError):
        await message.reply("Usage: /addsudo <user_id>")
        return

    if user_id not in db["sudo_users"]:
        db["sudo_users"].append(user_id)
        await message.reply(f"User {user_id} has been added as a sudo user.")
    else:
        await message.reply("This user is already a sudo user.")

@dp.message_handler(commands=['removesudo'])
async def remove_sudo_user(message: types.Message):
    """Remove a sudo user. Only the owner can use this command."""
    if message.from_user.id != OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    # Extract user ID to remove from the command arguments
    try:
        args = message.text.split()
        user_id = int(args[1])
    except (IndexError, ValueError):
        await message.reply("Usage: /removesudo <user_id>")
        return

    if user_id in db["sudo_users"]:
        db["sudo_users"].remove(user_id)
        await message.reply(f"User {user_id} has been removed as a sudo user.")
    else:
        await message.reply("This user is not a sudo user.")

@dp.message_handler(commands=['checksudo'])
async def check_sudo_user(message: types.Message):
    """Check if the user is a sudo user."""
    if message.from_user.id == OWNER_ID:
        await message.reply("You are the owner and have sudo access.")
        return

    if message.from_user.id in db["sudo_users"]:
        await message.reply("You are a sudo user.")
    else:
        await message.reply("You are not a sudo user.")

# Remaining handlers...

if __name__ == '__main__':
    logger.info("Starting Edit Guardian Bot with owner functionality...")
    executor.start_polling(dp, skip_updates=True)
