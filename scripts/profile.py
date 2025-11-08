from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.enums import ParseMode
from scripts.jsons import jsonUpdater
from scripts.sql import sqlDB

rProfile: Router = Router()
base: str = jsonUpdater.base
profs: str = jsonUpdater.profs
dbPath: str = "database/stats.db"


# ====| /PROFILE [ARGS] |=== #
@rProfile.message(Command('profile', 'профиль'))
async def get_props(message: Message, command: CommandObject):
    messageSend = False
    userName: str = message.from_user.username

    if base["blacklist"].count(message.from_user.username):
        for i in base["commands"]["ban"]:
            answer += i
    else:

        if command.args is None:
            await message.reply(
                text="Команда для поиска профилей пользователей в боте. Необходим запрос в виде: <code>/profile ник</code>", parse_mode=ParseMode.HTML
            )
            messageSend = True

        else:
            if profs.get(command.args.upper()):
                    answer: str = ""
                    answer = "<b>" + profs[command.args.upper()]["link"] + "</b>" + " |  <i>" + profs[command.args.upper()]["role"] + "</i>" + "\n" + "<u>Статус:</u> " + profs[command.args.upper()]["status"] + "\n\n" + "<u>О себе:</u> " + profs[command.args.upper()]["desc"] + "\n\n" + "<u>Награды:</u>\n" + "<blockquote expandable>" + profs[command.args.upper()]["awards"] + "</blockquote>\n\n" + "<u>Проекты:</u>\n" + "<blockquote expandable>" + profs[command.args.upper()]["projects"] + "</blockquote>\n\n"

                    await message.reply(
                        text=answer, parse_mode=ParseMode.HTML
                    )
                    messageSend = True
                    sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="profile", rowid=1)
            else:
                pass
    
    if messageSend == False:
        username: str = message.from_user.username
        await message.reply(
        text="Введеный вами пользователь не был найдет в базе данных бота. Перепроверьте правильность его написания!\n\nВы также можете сообщить об этом в нашей группе ТГ", parse_mode=ParseMode.HTML
        )
        sqlDB.setDatas(sqlDB, tableName="requests", valuesArr=[str(userName)+" "+str(message.from_user.id), "profile", command.args])
# ====| /PROFILE [ARGS] |=== #