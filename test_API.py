import requests
import allure
import pytest


base_url = "https://ariadne.aviasales.com/api/gql"
headers = {
        'accept': 'application/json',
        'accept-language': 'ru,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.aviasales.ru',
        'referer': 'https://www.aviasales.ru/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0\
                YaBrowser/25.2.0.0 Safari/537.36'
        }


@pytest.mark.api
@allure.title("Тест с отсутствующей датой")
@allure.description("Этот тест проверяет обработку случая,\
                     когда дата отправления не указана.")
def test_date_none() -> str:
    url = base_url
    header = headers
    future_date = ""
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

        fragment airlinesFields on Airline { iata \
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
                    "depart_dates": [future_date],
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

    response = requests.post(url, json=data, headers=header)

    assert response.status_code == 400, "Ожидаемый статус \
        ответа 400, так как дата не указана."
    result = response.json()
    assert 'data' in result, "Ключ 'data' отсутствует в ответе"
    assert result['data'] is None, "'data' должно быть равно None"
    assert 'errors' in result, "Ключ 'errors' отсутствует в ответе"
    assert any(
        "invalid" in error['message'] for error in result['errors']
        ), "Ошибка не содержит слово 'invalid'"


@pytest.mark.api
@allure.title("Тест получения цен для нового города")
@allure.description("Этот тест проверяет получение \
                    лучших цен для путешествия в новый город.")
def test_new_city() -> str:
    url = base_url
    header = headers
    future_date = "2025-04-01"
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
                    "depart_dates": [future_date],
                },
                "origin": "MOV",
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

    response = requests.post(url, json=data, headers=header)

    assert response.status_code == 200, "Ожидаемый статус ответа 200"
    result = response.json()

    assert 'data' in result, "Ключ 'data' отсутствует в ответе"
    assert result['data']['best_prices_v2'] is not None, "'best_prices_v2'\
          равно None"


@pytest.mark.api
@allure.title("Тест запроса с прошлой датой")
@allure.description("Этот тест проверяет ответ API для прошедшей даты.")
def test_past_date_query() -> str:
    url = base_url
    header = headers
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

    response = requests.post(url, json=data, headers=header)

    # Проверяем статус ответа
    assert response.status_code == 400, "Ожидаемый код состояния 400"

    result = response.json()
    assert 'data' in result, "Ключ 'data' отсутствует в ответе"
    assert result['data'] is not None, "'data' равно None"
    assert 'errors' in result, "Ключ 'errors' отсутствует в ответе"
    assert any(
        "invalid" in error['message'] for error in result['errors']
        ), "Сообщение об ошибке не указывает на недействительную дату"


@allure.step("Отправка запроса на получение лучших цен")
def send_request(url, data, headers):
    return requests.post(url, json=data, headers=headers)


@pytest.mark.api
@allure.feature("Тестирование API Aviasales")
@allure.story("Получение лучших цен в одну сторону")
def test_way1() -> str:
    url = base_url
    header = headers

    future_date = "2025-04-01"
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

        fragment airlinesFields on Airline { iata \
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
                    "depart_dates": [future_date],
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

    response = send_request(url, data, header)

    assert response.status_code == 200, f"Неверный\
          статус ответа: {response.status_code}"
    result = response.json()

    assert 'data' in result, "Ключ 'data' отсутствует в ответе"
    assert result['data']['best_prices_v2'] is not None, "'best_prices_v2'\
          равно None"


@pytest.mark.api
@allure.feature("Тестирование API Aviasales")
@allure.story("Получение лучших цен")
def test_way2() -> str:
    url = base_url
    header = headers
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

    response = send_request(url, data, header)

    assert response.status_code == 200, "Статус ответа не 200"
    result = response.json()

    assert 'data' in result, "Ключ 'data' отсутствует в ответе"
    assert result['data']['best_prices_v2'] is not None, "'best_prices_v2'\
          равно None"
