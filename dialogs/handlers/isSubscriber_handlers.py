from aiogram import Router
from aiogram.types import Message
from filters.filters import IsSubscriber, IsPrivatChat
from lexicon.lexicon import LEXICON

router = Router()


# Этот хэндлер будет реагировать на любые сообщения
# не от подписчиков канала
@router.message(IsPrivatChat, ~IsSubscriber())
async def send_echo(message: Message):
    await message.answer(LEXICON['channel_left'])
