from aiogram_dialog import DialogManager


# основной геттер
async def get_data(dialog_manager: DialogManager, **kwargs) -> dict | list:

    advertising_seo = [
        ("Реклама", 'Реклама'),
        ("SEO", 'SEO'),
        ("Реклама + SEO", 'Реклама + SEO')

    ]
    advertising_seo_data = dialog_manager.dialog_data.get('advertising_seo')

    customer_settings = {
        "advertising_seo": advertising_seo,
        "advertising_seo_data": advertising_seo_data,
    }

    return customer_settings


# геттер для вывода результата по выбранным настройкам
async def pars_sitings(dialog_manager: DialogManager, **kwargs) -> dict:

    advertising_seo = dialog_manager.dialog_data['advertising_seo']
    input_requests = '\n'.join([x.strip() for x in dialog_manager.dialog_data['input_requests']])
    input_region = dialog_manager.dialog_data['input_region'][0]

    result = {
        'advertising_seo': advertising_seo,
        'input_requests': input_requests,
        'input_region': input_region
    }

    return result
