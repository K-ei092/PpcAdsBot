import logging
import operator

from aiogram.enums import ContentType
from aiogram.fsm.state import StatesGroup, State

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Column, Next, Radio, Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.getters.general_getters import get_data, pars_sitings
from app.dialogs.handlers.general_handlers import (
    correct_input_handler,
    no_text,
    error_handler,
    parsing_data,
    radio_clicked_general
)

from app.lexicon.lexicon import LEXICON, LEXICON_TRANSITION
from app.utils.utils import requests_check, region_check


logger = logging.getLogger(__name__)


class DialogSG(StatesGroup):
    advertising_seo = State()
    input_requests = State()
    input_region = State()
    result = State()


main_dialog = Dialog(

    Window(
        Const(text=LEXICON['start']),
        Column(
            Radio(
                checked_text=Format(LEXICON_TRANSITION['radio_checked_text']),
                unchecked_text=Format(LEXICON_TRANSITION['radio_unchecked_text']),
                id='id_advertising_seo',
                item_id_getter=operator.itemgetter(1),
                items="advertising_seo",
                on_state_changed=radio_clicked_general
            ),
        ),
        Next(Const(LEXICON_TRANSITION['next']), when='advertising_seo_data'),
        state=DialogSG.advertising_seo,
        getter=get_data
    ),

    Window(
        Const(text=LEXICON['^collect^']),
        TextInput(
            id='input_requests',
            type_factory=requests_check,
            on_success=correct_input_handler,
            on_error=error_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        state=DialogSG.input_requests
    ),

    Window(
        Const(text=LEXICON['region']),
        TextInput(
            id='input_region',
            type_factory=region_check,
            on_success=correct_input_handler,
            on_error=error_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        state=DialogSG.input_region
    ),

    Window(
        Format(text=LEXICON['result_text']),
        Button(
            Const(LEXICON_TRANSITION['next_2']),
            id="parsing",
            on_click=parsing_data,
        ),
        SwitchTo(
            text=Const(
                LEXICON_TRANSITION['cancel']),
            id='cancel_dialog',
            state=DialogSG.advertising_seo),
        state=DialogSG.result,
        getter=pars_sitings
    ),
)
