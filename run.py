import json
import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from scripts.handlers import router
from scripts.donute import rDonute
from scripts.request import rRequest
from scripts.dev import rDev
from scripts.profile import rProfile
from scripts.tricks import rTricks

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(router, rDonute, rRequest, rDev, rProfile, rTricks)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

# /start            - worked!
# /donors           - worked!
# /help             - worked!
# /search [args]    - worked!
# /methods [args]   - worked!
# /props [args]     - worked!

# /test             - worked!
# /jsonUpdate       - worked!
# /stats            - worked!
# /send             - worked!
# /сommit [args]    - worked!

# /profile [args]   - worked!

# /request [args]   - worked!

# /buy [args]       - worked!
# /refund [args]    - worked!