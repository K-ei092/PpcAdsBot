from difflib import get_close_matches
from app.lexicon.city import LIST_CITY


# Проверка запроса на то, что он содержит не более 3 ключевых фраз, разделённых запятыми
def requests_check(text: str) -> str:
    if len(text.split(',')) <= 3:
        return text
    raise ValueError('requests error')


# Проверка введённого города на то, что он содержится в списке доступных городов / регионов (на основе Яндекс Вордстар)
def region_check(text: str) -> str:
    city = get_close_matches(text, LIST_CITY, n=1, cutoff=0.8)
    if city:
        return city
    raise ValueError('region error')
