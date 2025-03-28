import requests
import allure


@allure.step("Отправка запроса на получение лучших цен")
def send_request(url, data, headers):
    return requests.post(url, json=data, headers=headers)


@allure.feature("Тестирование API Aviasales")
@allure.story("Получение лучших цен")
def test_way2() -> str:
    url = "https://ariadne.aviasales.com/api/gql"
    headers = {
        'accept': 'application/json',
        'accept-language': 'ru,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.aviasales.ru',
        'referer': 'https://www.aviasales.ru/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 \
                YaBrowser/25.2.0.0 Safari/537.36'
    }

    departure_date = "2025-04-01"
    return_date = "2025-04-15"
    data = {
        "query": """
        query GetBestPricesV2($input: BestPricesV2Input!, \
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
        fragment citiesFields on CityInfo { city { iata \
            translations(filters: {locales: $locales}) } }
        fragment airportsFields on Airport { iata city { iata } }
        """,
        "variables": {
            "brand": "AS",
            "locales": ["ru"],
            "input": {
                "currency": "rub",
                "dates": {
                    "depart_dates": [departure_date],
                    "return_dates": [return_date],
                },
                "origin": "KUF",
                "destination": "PEZ",
                "one_way": False,
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

    response = send_request(url, data, headers)

    assert response.status_code == 200, "Статус ответа не 200"
    result = response.json()

    assert 'data' in result, "Ключ 'data' отсутствует в ответе"
    assert result['data']['best_prices_v2'] is not None, "'best_prices_v2'\
          равно None"
