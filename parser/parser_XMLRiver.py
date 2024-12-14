import time

import requests
import logging

from configuration.config import ConfigBot, load_config_bot


logger = logging.getLogger(__name__)


class ParserClient:

    def __init__(self):
        self.session = None
        self.config_xmlriver: ConfigBot = load_config_bot()
        self.USER_ID_xmlriver: str = self.config_xmlriver.tg_bot.user_id_xmlriver
        self.KEY_xmlriver: str = self.config_xmlriver.tg_bot.api_key_xmlriver
        self.url: str = 'http://xmlriver.com/search_yandex/xml?'

    def _get_string(self, s: str) -> str:
        """Обрабатывает строку, заменяя символы и удаляя лишние пробелы."""

        if "&" in s:
            s = s.replace("&", "%26")  # Заменяем символ '&' на '%26'
        return '+'.join(s.split())  # Удаляем лишние пробелы

    def open_session(self):
        """Создает и возвращает новую сессию requests."""

        self.session = requests.Session()
        return self.session

    def get_response(self, session, region, client_request, num_page, timeout):
        """Отправляет запрос и возвращает ответ."""

        client_request = self._get_string(client_request)
        params = {
            'user': self.USER_ID_xmlriver,
            'key': self.KEY_xmlriver,
            'lr': region,
            'query': client_request,
            'lang': 'ru',
            'device': 'desktop',
            'page': num_page
        }

        for attempt in range(3):  # Повторяем запрос до 3 раз

            try:
                response = session.get(url=self.url, params=params, timeout=timeout)
                response.raise_for_status()  # Вызывает исключение для ошибок HTTP
                if '<error code="' in response.text:
                    logger.info(f"Ошибка на сервере {response.text.split('error')[1]}")
                    if attempt < 2:
                        time.sleep(0.5)
                        continue
                    else:
                        error = response.text.split('error')[1]
                        return f"Ошибка на сервере {error}"
                else:
                    return response.text

            except requests.exceptions.Timeout:
                logger.info("Время ожидания запроса истекло.")
                return "Ошибка. Время ожидания запроса истекло."
            except requests.exceptions.RequestException as e:
                logger.info(f"Ошибка при запросе: {e}")
                return "Ошибка при выполнении запроса."
            except ValueError:
                logger.info("Ошибка при обработке ответа.")
                return "Ошибка при обработке ответа."


# Пример использования:
if __name__ == "__main__":
    parser_client = ParserClient()
    session = parser_client.open_session()
    response = parser_client.get_response(session, region='213', client_request='заборы для дачи', num_page=1,
                                          timeout=30)
    print(response)
