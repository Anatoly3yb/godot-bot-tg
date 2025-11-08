from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.enums import ParseMode
from scripts.jsons import jsonUpdater
from scripts.sql import sqlDB
from config import ADMIN

rDev: Router = Router()

# ====| CONTROL COMMAND |=== #
# ]==================================          ] TEST [

@rDev.message(Command('test', 'тест'))
async def cmd_test(message: Message):
    if message.from_user.id == ADMIN:
        answer: str = '<tg-emoji emoji-id="5327962748082995135">👍</tg-emoji>'  #"<a href='http://www.example.com/'>inline URL</a>"
        await message.reply(
            text=answer,
            parse_mode=ParseMode.HTML)
    
# ]==================================          ] TEST [



# ]==================================          ] JSONUPDATE [

@rDev.message(Command('jsonUpdate', 'обновиДсон'))
async def get_update(message: Message):
    if message.from_user.id == ADMIN:
        jsonUpdater.updateJson(jsonUpdater)
        await message.answer('База данных обновлена')

# ]==================================          ] JSONUPDATE [



# ]==================================          ] STATS [

@rDev.message(Command('stats', 'статистика'))
async def get_update(message: Message):

    if message.from_user.id == ADMIN:
        arrCommand = sqlDB.getData(sqlDB, "analytics")
        answer: str = ""

        arrRequests = sqlDB.getDatas(sqlDB, "requests", 10)
        if arrRequests != []:
            answer += "\n" + " От: <b>@" + arrRequests[0][0] + "</b> | <u>Команда:</u> <code>/" + arrRequests[0][1] + "</code> | <u>Запрос:</u> <blockquote expandable>" + arrRequests[0][2] + "</blockquote>"
        else:
            answer == ""
        await message.answer("<b>Статистика по командам:</b>\n\n<blockquote>start: " + str(arrCommand[0]) + "\nhelp: " + str(arrCommand[1]) + "\nsupport: " + str(arrCommand[2]) + "\nsearch: " + str(arrCommand[3]) + "\nmethods: " + str(arrCommand[4]) + "\nprops: " + str(arrCommand[5]) + "\nrequest: " + str(arrCommand[6]) + "\nprofile: " + str(arrCommand[7]) + "</blockquote>\n\nЗапросы:" + answer,
                             parse_mode=ParseMode.HTML)

# ]==================================          ] STATS [



# ]==================================          ] SEND [

@rDev.message(Command('send', 'написать'))
async def cmd_send(message: Message, command: CommandObject, bot: Bot):

    if message.from_user.id == ADMIN:

        if command.args is None:
            await message.reply(text="Необходимы аргументы") 
            
        else:
            try:
                args = command.args.split("-")
                id: int = int(args[0]) 
                answer: str = str(args[1])

                await bot.send_message(
                    chat_id=id, 
                    text=answer, 
                    parse_mode=ParseMode.HTML
                ) 
            except:
                await message.reply(text="Неверно использована команда Пример: /send userId-answerText")

# ]==================================          ] SEND [



# ]==================================          ] COMMIT [

@rDev.message(Command('commit', 'запись', 'изменение'))
async def cmd_send(message: Message, command: CommandObject, bot: Bot):

    if command.args is None:
        await message.reply(text="Необходимы аргументы. <code>/commit [Тема]-[Ваша запись]</code>.\n\nУчтите! Между темой и первым словом вашей записи должен стоять знак '-' (тире).\n\n<blockquote expandable><b>Руководство по стилю написания: </b>необходимо после знака '-' ставить перенос на вторую строку. Вторая строка является заголовком для объекта, форматируется как жирный шрифт. Третья строка остается пустой, разделяя заголовок и краткое описание. Описание начинается с четвертой строки. \n\nПримечания, большой текст рекомендуется заключать в Цитаты. \n\nАнглицизмы, методы, названия объектов, значения выделяются как моноширинный шрифт.</blockquote>\n\nВаша заявка будет направлена администрации и отформатирована в нужном стиле, но рекомендуется следовать нашему руководству!", parse_mode=ParseMode.HTML) 
           
    else:
        try:
            args = command.args.split("-")
            theme: str = str(args[0])

            await bot.send_message(
                chat_id=ADMIN, 
                text="Тема: " + theme + "\n\n" + message.html_text + "\n\nОт пользователя: @%s ID: %s" %(message.from_user.username, message.from_user.id), 
                parse_mode=ParseMode.HTML
            ) 
        except:
            await message.reply(text="Неверно использована команда Пример: <code>/commit Node2D-2D-игровой объект, наследуемый всеми 2D-узлами. Имеет положение, вращение, масштаб и наклон.</code>.\n\nУчтите! Между темой и первым словом вашей записи должен стоять знак '-' (тире)", parse_mode=ParseMode.HTML)

# ]==================================          ] COMMIT [

# ====| CONTROL COMMAND |=== #