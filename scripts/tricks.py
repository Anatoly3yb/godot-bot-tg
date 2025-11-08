from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from scripts.jsons import jsonUpdater
from scripts.sql import sqlDB

rTricks: Router = Router()

jsonUpdater.updateJson(jsonUpdater)

base: dict = jsonUpdater.base
tricks: dict = jsonUpdater.tricks


kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back'), 
     InlineKeyboardButton(text='Вперед', callback_data='forward')],
    [InlineKeyboardButton(text='Скрыть', callback_data='clear')]
])


@rTricks.message(Command('tricks'))
async def cmd_tricks(message: Message, command: CommandObject):
    messageSend = False
    userName: str = message.from_user.username

    if base["blacklist"].count(userName):
        await message.reply(
            text="Отказано.", parse_mode=ParseMode.HTML)
        messageSend = True

    else:
        if command.args is None:
            await message.reply(
            text=tricks["0"]["body"]["0"], parse_mode=ParseMode.HTML
            )
            messageSend = True

        else:
            answer: str = ""
            #lists: list = []
            for index in tricks:
                if tricks[index]["tags"].count(command.args.upper()):

                    for item in tricks[index]["body"][str(command.args)]:
                        answer += item
                    
                    await message.reply(
                        text=answer, reply_markup=kb, parse_mode=ParseMode.HTML
                    )
                    answer = ""
                    messageSend = True
                    sqlDB.incrementValue(sqlDB, tableName="analytics", paramName="tricks", rowid=1)
            else:
                pass
    
    if messageSend == False:
        await message.reply(
            text="Данная фишка не была найдена. Перепроверьте правильность его написания!\n\nВы также можете сообщить об этом в нашей группе ТГ", parse_mode=ParseMode.HTML
        )
        #sqlDB.setDatas(sqlDB, tableName="requests", valuesArr=[str(userName)+" "+str(message.from_user.id), "methods", command.args])



@rTricks.callback_query(F.data == 'back')
async def cmd_back(callback: CallbackQuery):
    await callback.answer('Вы переместились назад')
    global pageNum
    
    if pageNum == 0:
        answer = getAnswer(tricks[str(courseId)]["body"], 0)
    else:
        pageNum = pageNum - 1
        answer = getAnswer(tricks[str(courseId)]["body"], pageNum)

    if callback.message.html_text != answer:
        await callback.message.edit_text(text=answer, reply_markup=kb, parse_mode=ParseMode.HTML)
    else:
        print("Сообщение не было изменено. Пользователь находится на той же странице")


@rTricks.callback_query(F.data == 'forward')
async def cmd_forward(callback: CallbackQuery):
    await callback.answer('Вы переместились вперед')
    answer: str = ""

    global pageNum
    global pageMax

    if pageNum == pageMax:
        answer = getAnswer(tricks[str(courseId)]["body"], pageMax)

    if pageNum < pageMax:
        pageNum = pageNum + 1
        answer = getAnswer(tricks[str(courseId)]["body"], pageNum)

    if callback.message.html_text != answer:
        await callback.message.edit_text(text=answer, reply_markup=kb, parse_mode=ParseMode.HTML)
    else:
        print("Сообщение не было изменено. Пользователь находится на той же странице")


@rTricks.callback_query(F.data == 'clear')
async def cmd_delete(callback: CallbackQuery):
    await callback.answer('Фишка была скрыта')
    await callback.message.delete()