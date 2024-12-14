import time

import requests
import logging

from app.configuration.config import ConfigBot, load_config_bot


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


# <?xml version="1.0" encoding="UTF-8" ?>
# <yandexsearch version="1.0">
#   <response date="20241209T185033"><error code="500">Выполните перезапрос. Ответ от поисковой системы не получен.</error></response></yandexsearch>

# <?xml version="1.0" encoding="UTF-8" ?>
# <yandexsearch version="1.0">
#   <response date="20241209T185337"><found priority="all">3000000</found><advcount>2</advcount><topads><query><url>http://masterovit.ru</url><adsurl></adsurl><title>Закажи %3Cb%3Eзабор%3C/b%3E %3Cb%3Eдля%3C/b%3E %3Cb%3Eдачи%3C/b%3E сейчас! В 2025 будет дороже!</title><snippet>Закажите детальный расчет %3Cb%3Eзабора%3C/b%3E! Скидка до 23%! Гарантия до 5 лет! Доставка 0 руб*!Выезд до 350 км от МКАД. Свое производство. Нам доверяют 25 лет</snippet><oneline><sitelink><title>Акции и Скидки</title><url>http://Акции и Скидки</url></sitelink><sitelink><title>Доставка0₽*</title><url>http://Доставка0₽*</url></sitelink><sitelink><title>Выезд менеджера</title><url>http://Выезд менеджера</url></sitelink><sitelink><title>Гарантия до 5лет</title><url>http://Гарантия до 5лет</url></sitelink></oneline></query><query><url>http://market.yandex.ru</url><adsurl></adsurl><title>Заборные материалы — купить на Яндекс Маркете</title><snippet>Зеленые цены на Яндекс Маркете. Покупайте выгодно. Платите по частям со Сплитом.Честные отзывы. Быстрая доставка. Доставка по клику. Оплата со сплитом</snippet><oneline><sitelink><title>Электроинструменты</title><url>http://Электроинструменты</url></sitelink><sitelink><title>Электрика</title><url>http://Электрика</url></sitelink><sitelink><title>Сантехника</title><url>http://Сантехника</url></sitelink><sitelink><title>Отделочные материалы</title><url>http://Отделочные материалы</url></sitelink></oneline></query></topads><bottomads><query><url>http://zabor-sad.ru</url><adsurl></adsurl><title>%3Cb%3EЗабор%3C/b%3E на %3Cb%3Eдачу%3C/b%3E цена с установкой. Скидки до&amp;nbsp,17%!…</title><snippet>%3Cb%3EЗабор%3C/b%3E на %3Cb%3Eдачу%3C/b%3E цена с установкой. Работаем под ключ +Более 10 лет! Низкие цены! Жмите!Без предоплаты. Калькулятор. Гарантия на работы 2 года. Выезд замерщика бесплатно</snippet><oneline><sitelink><title>Материалы высокого качества</title><url>http://Материалы высокого качества</url></sitelink><sitelink><title>Профнастил</title><url>http://Профнастил</url></sitelink><sitelink><title>Сетка</title><url>http://Сетка</url></sitelink><sitelink><title>Евроштакетник</title><url>http://Евроштакетник</url></sitelink></oneline></query><query><url>http://zaborvam.ru</url><adsurl></adsurl><title>Закажите %3Cb%3Eзабор%3C/b%3E %3Cb%3Eдля%3C/b%3E %3Cb%3Eдачи%3C/b%3E. Цена с установкой от 850 ₽/пм</title><snippet>3D-проект. Работа по договору. Выезд замерщика 0 ₽. Фиксированные цены. Звоните!Надежность. Долговечность. Детальные консультации. Хорошие отзывы</snippet><oneline><sitelink><title>14 лет опыта</title><url>http://14 лет опыта</url></sitelink><sitelink><title>Наши работы</title><url>http://Наши работы</url></sitelink><sitelink><title>Онлайн-калькулятор</title><url>http://Онлайн-калькулятор</url></sitelink><sitelink><title>Цены</title><url>http://Цены</url></sitelink></oneline></query><query><url>http://fensgar.ru</url><adsurl></adsurl><title>2d %3Cb%3EЗаборы%3C/b%3E от завода Fensgar</title><snippet>Минимальный заказ от 100м. Без посредников. Скидка 25% от 150м. Гарантия 50 лет.</snippet><oneline><sitelink><title>Доставка по России</title><url>http://Доставка по России</url></sitelink><sitelink><title>2D ограждения</title><url>http://2D ограждения</url></sitelink><sitelink><title>3D ограждения</title><url>http://3D ограждения</url></sitelink><sitelink><title>Звоните прямо сейчас</title><url>http://Звоните прямо сейчас</url></sitelink></oneline></query><query><url>http://zs77.ru</url><adsurl></adsurl><title>Купить %3Cb%3Eзабор%3C/b%3E с установкой сейчас или бронь на 2025</title><snippet>Держим цены. Собственное производство. Бесплатный выезд замерщика. Гарантии.</snippet></query></bottomads><results><grouping><page first="1" last="10">2</page><group id="1"><doccount>1</doccount><doc><url>https://zaborsad.ru/</url><title>Купить забор с установкой под ключ в Москве - Заборсад</title><contenttype>organic</contenttype><passages><passage>Заборы из профлиста для дачи.... Зелёный 3Д забор из сетки для дачного дома.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="2"><doccount>1</doccount><doc><url>https://good-zabor.ru/catalog/zabory-dlya-dachi.html</url><title>Заборы для дачи, цены на дачный забор с установкой...</title><contenttype>organic</contenttype><passages><passage>Наша компания проектирует и устанавливает заборы для дачи в Москве и Московской области.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="3"><doccount>1</doccount><doc><url>https://uslugi.yandex.ru/213-moscow/category?text=забор на дачу эконом вариант</url><title>Забор на дачу эконом вариант в Москве: 120 строителей...</title><contenttype>organic</contenttype><passages><passage>калитка забора, фотографии заборов, забор из профнастила, ограждение забор, металлический забор. дача, дом дача, дачен, дачнае, дачные участки.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="4"><doccount>1</doccount><doc><url>https://horoshie-zabory.ru/zabory-dlya-dachi/zabor-ekonom-variant/</url><title>Забор на дачу эконом вариант купить в Москве</title><contenttype>organic</contenttype><passages><passage>Заборы для дачи из профнастила в Видном.... Металлический забор для дачи из евроштакетника с воротами и калиткой.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="5"><doccount>1</doccount><doc><url>https://ZavodZaborov.ru/zabory-dlya-dachi/</url><title>Заборы для дачи под ключ, цены в Москве, изготовление...</title><contenttype>organic</contenttype><passages><passage>Цена на заборы для дачи зависит от выбранного материала, высоты и сложности конструкции.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="6"><doccount>1</doccount><doc><url>https://dostup-zabor.ru/zabory-dlya-dachi/zabor-ekonom-variant/</url><title>Забор на дачу эконом вариант купить в Москве | Цены...</title><contenttype>organic</contenttype><passages><passage>МОНТАЖ ВОРОТ И КАЛИТКИ Завершающий этап строительства забора на дачу эконом вариант — установка ворот.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="7"><doccount>1</doccount><doc><url>https://www.all-zabor.ru/zabory_dlya_dachi/</url><title>Купить заборы из профнастила для дачи в Москве...</title><contenttype>organic</contenttype><passages><passage>Строительство заборов из профнастила для дачи по низкой стоимости - заказать в Москве.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="8"><doccount>1</doccount><doc><url>https://забор-для-дачи.рф/</url><title>Заборы в Москве с установкой под ключ для дачи</title><contenttype>organic</contenttype><passages><passage>Компания «Забор для дачи» - специализируется на производстве и монтаж заборов для дачи и дома в Москве и Московской области.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="9"><doccount>1</doccount><doc><url>https://www.Moskovskie-zabory.ru/zabory-dlya-dachi/</url><title>Заборы для дачи, цена с установкой в Москве | Дачный...</title><contenttype>organic</contenttype><passages><passage>Заборы для дачи с установкой под ключ в Москве и области &amp;gt; Выгодные цены от производителя, быстрая доставка, монтаж за 1 день...</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group><group id="10"><doccount>1</doccount><doc><url>https://www.stroyzabor.ru/zabory-dlya-dachi/</url><title>Заборы для дачи в Москве, цена с установкой | Дачный...</title><contenttype>organic</contenttype><passages><passage>Приобретение забора для дачи - это серьезное дело, ведь он выполняет несколько функций: ограждение, эстетическое украшение и защиту.</passage></passages><tablesnippet></tablesnippet><extendedpassages></extendedpassages></doc></group></grouping></results></response></yandexsearch>
