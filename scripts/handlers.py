from aiogram import F, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from scripts.jsons import jsonUpdater
from scripts.sql import sqlDB

jsonUpdater.updateJson(jsonUpdater)

base: dict = jsonUpdater.base
docs: dict = jsonUpdater.docs
methods: dict = jsonUpdater.methods
props: dict = jsonUpdater.props
profs: dict = jsonUpdater.profs

router: Router = Router()



# ====| /START |=== #
@router.message(CommandStart())
async def cmd_start(message: Message):
    answer: str = ""

    if base["blacklist"].count(message.from_user.username):
        for i in base["commands"]["ban"]:
            answer += i
    
    else:
        for i in base["commands"]["start"]:
            answer += i
        sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="start", rowid=1)
    
    await message.reply(
        text=answer, parse_mode=ParseMode.HTML)
# ====| /START |=== #



# ====| /DONORS |=== #
@router.message(Command('donors', 'доноры', 'спонсоры'))
async def cmd_start(message: Message):
    answer: str = ""

    if base["blacklist"].count(message.from_user.username):
        for i in base["commands"]["ban"]:
            answer += i
        
    else:
        for i in base["commands"]["donors"]["body"]:
            answer += i

        for idx in base["commands"]["donors"]["sponsors"]:

            if idx == "Платиновые спонсоры":
                donorsArr: list = sqlDB.getFilterDatas(sqlDB, tableName="donors", filterName="PLATINUM", limit=100)
            if idx == "Золотые спонсоры":
                donorsArr: list = sqlDB.getFilterDatas(sqlDB, tableName="donors", filterName="GOLD", limit=100)
            if idx == "Серебрянные спонсоры":
                donorsArr: list = sqlDB.getFilterDatas(sqlDB, tableName="donors", filterName="SILVER", limit=100)
            # TODO ВЫВОДИТ МНОГО ОДНОТИПНЫХ СПИСКОВ
            if donorsArr == []:
                pass
            else:
                for index in range(len(donorsArr)):
                    answer += "\n\n%s:\n<blockquote expandable>@%s</blockquote>" % (idx, donorsArr[index][0])

        sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="donors", rowid=1)

    answer += base["commands"]["donors"]["end"]

    await message.reply(
                text=answer, disable_web_page_preview=True, parse_mode=ParseMode.HTML
            )
# ====| /DONORS |=== #



# ====| /HELP |=== #
@router.message(Command('help', 'помощь', 'помоги'))
async def cmd_help(message: Message):
    answer: str = ""

    if base["blacklist"].count(message.from_user.username):
        for i in base["commands"]["ban"]:
            answer += i

    else:
        for i in base["commands"]["help"]:
            answer += i
        sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="help", rowid=1)

    await message.reply(
        text=answer, parse_mode=ParseMode.HTML)
# ====| /HELP |=== #



# ====| /SEARCH [ARGS] |=== #
@router.message(Command('search', 'поиск'))
async def get_search(message: Message, command: CommandObject):
    messageSend: bool = False
    answer: str = ""
    userName: str = message.from_user.username

    if base["blacklist"].count(message.from_user.username):
        await message.reply(
            text="Отказано.", parse_mode=ParseMode.HTML)
        messageSend = True

    else:
        if command.args:
            for index in docs:
                if docs[str(index)]["tags"].count(command.args.upper()):
                    for i in docs[str(index)]["body"]:
                        answer += i
                    buttonMarkup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=docs[str(index)]["button"]["text"], url=docs[str(index)]["button"]["link"])]])
                    await message.reply(
                        text=answer, reply_markup=buttonMarkup, parse_mode=ParseMode.HTML
                    )
                    messageSend = True
                    sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="search", rowid=1)

                else:
                    pass
        else:
            await message.reply(
            text="Команда для поиска в документации. Для поиска необходим запрос\n\nПримеры:\n* /search Types\n* /search Переменные", parse_mode=ParseMode.HTML
            )
            messageSend = True
    
    if messageSend == False:
        await message.reply(
        text="Информация на данную тему не была найдена, или возможно вы написали запрос с ошибкой!\n\nВы можете сообщить об этом в нашей группе ТГ", parse_mode=ParseMode.HTML
        )
        sqlDB.setDatas(sqlDB, tableName="requests", valuesArr=[str(userName)+" "+str(message.from_user.id), "search", command.args])

# ====| /SEARCH [ARGS] |=== #



# ====| /METHODS [ARGS] |=== #
@router.message(Command('methods', 'методы'))
async def get_methods(message: Message, command: CommandObject):
    messageSend = False
    userName: str = message.from_user.username

    if base["blacklist"].count(userName):
        await message.reply(
            text="Отказано.", parse_mode=ParseMode.HTML)
        messageSend = True
    else:

        if command.args is None:
            await message.reply(
            text="Команда для показа методов указанного объекта. Необходим запрос\n\nПримеры:\n* /methods AABB\n* /methods float", parse_mode=ParseMode.HTML
            )
            messageSend = True

        else:
            if methods.get(command.args.upper()):
                answer: str = ""
                for index in methods[command.args.upper()]["body"]:
                    for item in methods[command.args.upper()]["body"][index]:
                        answer += item
                    buttonMarkup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=methods[command.args.upper()]["button"]["text"], url=methods[command.args.upper()]["button"]["link"])]])
                    await message.reply(
                        text=answer, reply_markup=buttonMarkup, parse_mode=ParseMode.HTML
                    )
                    answer = ""
                    messageSend = True
                    sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="methods", rowid=1)
            else:
                pass
    
    if messageSend == False:
        await message.reply(
            text="Введеный вами объект не был найдет в базе данных. Перепроверьте правильность его написания!\n\nВы также можете сообщить об этом в нашей группе ТГ", parse_mode=ParseMode.HTML
        )
        sqlDB.setDatas(sqlDB, tableName="requests", valuesArr=[str(userName)+" "+str(message.from_user.id), "methods", command.args])
# ====| /METHODS [ARGS] |=== #



# ====| /PROPS [ARGS] |=== #
@router.message(Command('props', 'свойства'))
async def get_props(message: Message, command: CommandObject):
    messageSend = False
    userName: str = message.from_user.username

    if base["blacklist"].count(message.from_user.username):
        await message.reply(
            text="Отказано.", parse_mode=ParseMode.HTML)
        messageSend = True

    else:
        if command.args is None:
            await message.reply(
                text="Команда для показа свойств указанного объекта. Необходим запрос\n\nПримеры:\n* /props AABB\n* /props float", parse_mode=ParseMode.HTML
            )
            messageSend = True

        else:
            if props.get(command.args.upper()):
                answer: str = ""
                for i in props[command.args.upper()]:
                    answer += i
                await message.reply(
                    text=answer, parse_mode=ParseMode.HTML
                )
                messageSend = True
                sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="props", rowid=1)
            else:
                pass
    
    if messageSend == False:
        username: str = message.from_user.username
        await message.reply(
        text="Введеный вами объект не был найдет в базе данных. Перепроверьте правильность его написания!\n\nВы также можете сообщить об этом в нашей группе ТГ", parse_mode=ParseMode.HTML
        )
        sqlDB.setDatas(sqlDB, tableName="requests", valuesArr=[str(userName)+" "+str(message.from_user.id), "props", command.args])
# ====| /PROPS [ARGS] |=== #