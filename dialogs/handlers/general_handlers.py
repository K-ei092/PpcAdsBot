import logging
import os

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import ManagedRadio, Button

from lexicon.lexicon import LEXICON

from parser.adjuster import get_analysis

logger = logging.getLogger(__name__)


# хендлер на ввод корректных значений
async def correct_input_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:

    id_ = widget.widget.widget_id

    if id_ == 'input_requests':
        dialog_manager.dialog_data['input_requests']: list[str] = text.split(',')
    elif id_ == 'input_region':
        dialog_manager.dialog_data['input_region']: str = text

    # Удаляем ответ пользователя, удаляем прошлый и отправляем новый виджет
    await message.delete()
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


# хендлер на ввод неверных данных пользователем
async def error_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError) -> None:

    # удаляем ответ пользователя, устанавливаем мод в режим удаления и последующей отправки
    await message.delete()
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    error = error.__str__()

    if error == 'requests error':
        await message.answer(text=LEXICON['error_requests'])
    elif error == 'region error':
        await message.answer(text=LEXICON['error_region'])


# хендлер, когда пользователь отправил боту не текст
async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager) -> None:

    # удаляем ответ пользователя, устанавливаем мод в режим удаления и последующей отправки
    await message.delete()
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    await message.answer(text=LEXICON['no_text'])


# хендлер для записи данных выбранной радиокнопки
async def radio_clicked_general(
        callback: CallbackQuery,
        radio: ManagedRadio,
        dialog_manager: DialogManager,
        *args, **kwargs) -> None:

    id_ = callback.data.split(':')[0]
    item_id_getter = callback.data.split(':')[1]

    if id_ == 'id_advertising_seo':
        dialog_manager.dialog_data['advertising_seo']: str = item_id_getter


async def parsing_data(callback: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:

    await callback.answer(text=LEXICON['wait'])

    advertising_seo: str = dialog_manager.dialog_data['advertising_seo']
    input_requests: list[str] = dialog_manager.dialog_data['input_requests']
    input_region: str = dialog_manager.dialog_data['input_region'][0]

    await dialog_manager.reset_stack(remove_keyboard=True)

    result = get_analysis(advertising_seo, input_requests, input_region)

    if type(result) == str and result.endswith('.xlsx'):
        file = FSInputFile(result)
        await callback.message.answer(
            text="Ваш результат")
        await callback.message.answer_document(file)
        os.remove(result)
    else:
        await callback.message.answer(
            text=result
        )
