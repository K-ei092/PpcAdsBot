from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram_dialog import DialogManager, StartMode

from dialogs.main_dialog import DialogSG
from filters.filters import IsPrivatChat, IsSubscriber
from lexicon.lexicon import LEXICON


router = Router()


# хендлер на команду /start
@router.message(CommandStart(), IsPrivatChat(), IsSubscriber())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=DialogSG.advertising_seo, mode=StartMode.RESET_STACK)


# хендлер на команду /help
@router.message(Command(commands='help'), IsPrivatChat())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await message.answer(text=LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/help_region"
# и отправлять пользователю файл со списком доступных локаций яндекса
@router.message(Command(commands='help_region'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])
    file = FSInputFile('Region_yandex.txt')
    await message.answer_document(file)
