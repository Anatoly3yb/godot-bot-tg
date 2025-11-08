from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from scripts.jsons import jsonUpdater
from scripts.sql import sqlDB
from config import ADMIN

base: dict = jsonUpdater.base

rDonute: Router = Router()
CURRENCY = 'XTR'



def kb_payment(text: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text=text, pay=True)
    return kb_builder.as_markup()

# ====| /BUY |=== #
@rDonute.message(Command('buy', 'купить'))
async def cd_donute(message: Message, command: CommandObject, bot: Bot) -> None:
    messageSend: bool = False
    answer: str = ""
    
    if base["blacklist"].count(message.from_user.username):
        for i in base["commands"]["ban"]:
            answer += i
    else:
        if command.args is None:
            for idx in base["commands"]["buy"]:
                answer += idx
        else:
            if base["prices"].get(command.args.upper()):
                labalPrice = [LabeledPrice(label=CURRENCY, amount=int(base["prices"][command.args.upper()][2]))]
                
                await message.reply_invoice(
                    title=str(base["prices"][command.args.upper()][0]),
                    description=str(base["prices"][command.args.upper()][1]),
                    prices=labalPrice,
                    provider_token="",
                    payload=str(base["prices"][command.args.upper()][3]),
                    currency=CURRENCY,
                    reply_markup=kb_payment("Купить подписку за %s ⭐️" % (str(base["prices"][command.args.upper()][2]))),
                )
                messageSend = True
            else:
                answer = "не была найдена покупаемая услуга. Перепроверьте правильность ее написания"

    if messageSend == False:
        await message.reply(
            text=answer, parse_mode=ParseMode.HTML
        )

@rDonute.pre_checkout_query()
async def pre_checkout_handler(preCheckOut: PreCheckoutQuery):
    await preCheckOut.answer(ok=True)

@rDonute.message(F.successful_payment)
async def processSuccessfulPay(message: Message, bot: Bot):
    answer: str = ""

    sqlDB.setDatas(sqlDB, tableName="donors", valuesArr=[str(message.from_user.username), int(message.from_user.id), str(message.successful_payment.invoice_payload)])

    await message.reply(text="<u>ID покупки:</u> <code>" + f'{message.successful_payment.telegram_payment_charge_id}' + "</code>\n\nВы сможете его использовать для возврата средств, поэтому сохраните его!", message_effect_id="5104841245755180586", parse_mode=ParseMode.HTML)

    if message.successful_payment.invoice_payload == "PLATINUM":
        answer = "Куплена подписка: " + str(message.successful_payment.invoice_payload) + "\n\n<blockquote>ID пользователя: " + str(message.from_user.id) + "\nИмя пользователя: @" + str(message.from_user.username)+"</blockquote>"
    if message.successful_payment.invoice_payload == "GOLD":
        answer = "Куплена подписка: " + str(message.successful_payment.invoice_payload) + "\n\n<blockquote>ID пользователя: " + str(message.from_user.id) + "\nИмя пользователя: @" + str(message.from_user.username)+"</blockquote>"
    if message.successful_payment.invoice_payload == "SILVER":
        answer = "Куплена подписка: " + str(message.successful_payment.invoice_payload) + "\n\n<blockquote>ID пользователя: " + str(message.from_user.id) + "\nИмя пользователя: @" + str(message.from_user.username)+"</blockquote>"
    if message.successful_payment.invoice_payload == "DONUTE":
        answer = "Бота поддержали: " + str(message.successful_payment.invoice_payload) + "\n\n<blockquote>ID пользователя: " + str(message.from_user.id) + "\nИмя пользователя: @" + str(message.from_user.username)+"</blockquote>"

    await bot.send_message(
        chat_id=ADMIN, 
        text=answer, 
        parse_mode=ParseMode.HTML
        )


# ====| /REFUND |=== #
@rDonute.message(Command('refund', 'вернуть', 'возврат'))
async def cd_donute(message: Message, command: CommandObject, bot: Bot) -> None:
    messageSend: bool = False
    answer: str = ""

    if base["blacklist"].count(message.from_user.username):
        for i in base["commands"]["ban"]:
            answer += i
    
    else:
        if command.args is None:
            for idx in base["commands"]["refund"]:
                answer += idx
        else:
            transactId = command.args
            try:
                await bot.refund_star_payment(
                    user_id=message.from_user.id,
                    telegram_payment_charge_id=transactId
                )

                sqlDB.clearDatasUser(sqlDB, "donors", message.from_user.id)

                await bot.send_message(
                    chat_id=ADMIN, 
                    text="Возврат" + "\n<blockquote>ID пользователя: " + str(message.from_user.id) + "\nИмя пользователя: @" + str(message.from_user.username)+"</blockquote>", 
                    parse_mode=ParseMode.HTML
                )
                messageSend = True
            except:
                await message.reply(
                    text="Возврат средств не был произведен. Вероятно вы ввели неверный ID, или за этот ID уже был произведет возврат.", parse_mode=ParseMode.HTML
                )
                messageSend = True

    if messageSend == False:
        await message.reply(
            text=answer, parse_mode=ParseMode.HTML
        )