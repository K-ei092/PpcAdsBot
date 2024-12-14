import asyncio
import logging
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs

from dialogs.main_dialog import main_dialog

from dialogs.handlers import isSubscriber_handlers, main_handlers, other_handlers

from keyboards.main_menu import set_main_menu

from configuration.config import ConfigBot, load_config_bot


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():

    log_name = f'logs/{datetime.now().strftime("%Y-%m-%d")}.log'
    Path(log_name).parent.mkdir(parents=True, exist_ok=True)

    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.WARNING,                             # настройка - DEBUG, production - WARNING
        filename=log_name,                               # добавляем логи в файл
        filemode='w',                                      # режим записи (a - добавить, w - переписать)
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг
    config_bot: ConfigBot = load_config_bot()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config_bot.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML')  # 'MarkdownV2'
    )

    dp = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры (диалоги) в диспетчере
    dp.include_router(main_handlers.router)
    dp.include_router(main_dialog)
    dp.include_router(isSubscriber_handlers.router)
    dp.include_router(other_handlers.router)

    setup_dialogs(dp)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())
