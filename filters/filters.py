from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message
from configuration.config import ConfigBot, load_config_bot
from difflib import get_close_matches
from lexicon.city import LIST_CITY


config: ConfigBot = load_config_bot()
CHAT_ID = config.tg_bot.chat_id


# фильтр проверяющий, что сообщение пришло в приватном чате
class IsPrivatChat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type == 'private':
            return True
        else:
            return False


# Этот фильтр проверяет подписан ли пользователь на телеграм-канал
class IsSubscriber(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        for chat_id in CHAT_ID:
            sub = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            if sub.status != 'left':
                return True
            else:
                return False


# Этот фильтр проверяет есть ли введенная пользователем локация
# в списке доступных городов / регионов (на основе Яндекс Вордстар)
class CheckCity(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        city = get_close_matches(message.text, LIST_CITY, n=1, cutoff=0.8)
        if city:
            return True
        else:
            return False
