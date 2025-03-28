import requests
import allure


@allure.title("Тест запроса с прошлой датой")
@allure.description("Этот тест проверяет ответ API для прошедшей даты.")
def test_past_date_query() -> str:
    url = "https://ariadne.aviasales.com/api/gql"
    headers = {
        'accept': 'application/json',
        'accept-language': 'ru,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.aviasales.ru',
        'referer': 'https://www.aviasales.ru/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
              AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 \
                YaBrowser/25.2.0.0 Safari/537.36'
    }

    past_date = "2022-04-01"  # Прошедшая дата
    data = {
        "query": """
        query GetBestPricesV2($input: BestPricesV2Input!,\
              $brand: Brand!, $locales: [String!]) {
            best_prices_v2(input: $input, brand: $brand) {
                cheapest { ...priceFields }
                cheapest_direct { ...priceFields }
                cheapest_convenient { ...priceFields }
                places {
                    cities { ...citiesFields }
                    airlines { ...airlinesFields }
                    airports { ...airportsFields }
                }
            }
        }

        fragment priceFields on Price {
            depart_date
            return_date
            value
            ticket_link
            currency
        }

        fragment airlinesFields on Airline { iata\
              translations(filters: {locales: $locales}) }
        fragment citiesFields on CityInfo { city { iata\
              translations(filters: {locales: $locales}) } }
        fragment airportsFields on Airport { iata city { iata } }
        """,
        "variables": {
            "brand": "AS",
            "locales": ["ru"],
            "input": {
                "currency": "rub",
                "dates": {
                    "depart_dates": [past_date],
                },
                "origin": "KUF",
                "destination": "PEZ",
                "one_way": True,
                "market": "ru",
                "filters": {
                    "no_visa_at_transfer": False,
                    "with_baggage": False,
                    "direct": False
                }
            }
        },
        "operation_name": "best_prices_v2"
    }

    response = requests.post(url, json=data, headers=headers)

    # Проверяем статус ответа
    assert response.status_code == 400, "Ожидаемый код состояния 400"

    result = response.json()
    assert 'data' in result, "Ключ 'data' отсутствует в ответе"
    assert result['data'] is not None, "'data' равно None"
    assert 'errors' in result, "Ключ 'errors' отсутствует в ответе"
    assert any(
        "invalid" in error['message'] for error in result['errors']
        ), "Сообщение об ошибке не указывает на недействительную дату"
