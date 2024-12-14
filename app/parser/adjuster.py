from app.parser.file_generetor import FileGenerator

from app.parser.parser_XMLRiver import ParserClient


def get_analysis(advertising_seo, input_requests, input_region):

    name_file = f'{input_requests[0] + "..."}_{input_region}.xlsx'

    result = ''

    fg = FileGenerator(advertising_seo, input_region, name_file)

    parser_client = ParserClient()
    with parser_client.open_session() as session:
        for input_request in input_requests:
            for num_page in range(2):
                response = parser_client.get_response(
                    session, region=input_region, client_request=input_request, num_page=num_page, timeout=30
                )
                if 'Ошибка' not in response:
                    result = fg.generate_file(response, input_request)
                else:
                    result = response
    fg.add_calculation_sheet()
    return result
