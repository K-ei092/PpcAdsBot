from dataclasses import dataclass
from environs import Env


@dataclass(slots=True, frozen=True)
class TgBot:
    token: str              # Токен для доступа к телеграм-боту
    admin_ids: list[int]    # Список id администраторов бота
    chat_id: list[int]      # Список чатов для подписки пользователем
    user_id_xmlriver: str   # ID пользователя xmlriver.com
    api_key_xmlriver: str   # Токен для доступа к xmlriver.com


@dataclass(slots=True, frozen=True)
class ConfigBot:
    tg_bot: TgBot


# функция для загрузки конфигрурации бота
def load_config_bot(path: str | None = None) -> ConfigBot:
    env = Env()
    env.read_env(path)
    return ConfigBot(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            chat_id=list(map(int, env.list('CHAT_ID'))),
            user_id_xmlriver=env('USER_ID_XMLRIVER'),
            api_key_xmlriver=env('API_KEY_XMLRIVER'),
        )
    )
