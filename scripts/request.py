from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.enums import ParseMode
from scripts.jsons import jsonUpdater
from config import ADMIN
from scripts.sql import sqlDB

base: str = jsonUpdater.base
rRequest: Router = Router()

# ====| /REQUEST |=== #
@rRequest.message(Command('request', 'запрос'))
async def cmd_request(message: Message, command: CommandObject, bot: Bot):

    if base["blacklist"].count(message.from_user.username):
        await message.reply(
            text="Отказано.", parse_mode=ParseMode.HTML)

    else:
        if command.args is None:
            answer: str = ""
            for i in base["commands"]["request"]:
                answer += i
            await message.reply(
                text=answer, parse_mode=ParseMode.HTML
            )
        else:
            await message.reply(
                text="Ваш запрос был отправлен", parse_mode=ParseMode.HTML)
            sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="request", rowid=1)
            
            await bot.send_message(
                chat_id=ADMIN, 
                text="Запрос:" + "\n\n<blockquote>" + command.args + "</blockquote>" + "\n\nID пользователя: " + str(message.from_user.id) + "\nИмя пользователя: @" + str(message.from_user.username), 
                parse_mode=ParseMode.HTML
            )     
# ====| /REQUEST |=== #