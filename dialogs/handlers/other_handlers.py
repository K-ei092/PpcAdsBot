from aiogram import Router
from aiogram.types import Message

from filters.filters import IsPrivatChat, IsSubscriber

router = Router()


@router.message(IsPrivatChat, IsSubscriber())
async def send_echo(message: Message):
    await message.answer(
        text=f'Мне неизвестна команда (или город) "{message.text}"\n'
             'Попробуй набрать /start или проверить наличие локации '
             'в списке через команду /help_region'
    )
