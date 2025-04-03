import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.aviasales.ru/?params=MOW1")
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def driverGOJ():
    driver = webdriver.Chrome()
    driver.get("https://www.aviasales.ru/?params=GOJ1")
    yield driver
    driver.quit()


@pytest.mark.ui
@allure.feature("Тестирование поиска авиабилетов")
@allure.story("Проверка ввода городов отправления \
               и назначения с заглавными буквами")
@allure.title("Проверка корректного заполнения\
               полей с заглавными буквами")
def test_CAPSname(driver) -> str:
    # Ввод города отправления
    with allure.step("Ввод города отправления 'МОСКВА'"):
        origin = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_origin-input"
                ))
        )
        origin.send_keys(Keys.CONTROL + "a")
        origin.send_keys(Keys.BACKSPACE)
        origin.send_keys("МОСКВА")

    # Ввод города назначения
    with allure.step("Ввод города назначения 'Пенза'"):
        destination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_destination-input"
                ))
        )
        destination.click()
        DestInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='search-destination-input']"
                ))
        )
        DestInput.send_keys("Пенза")
        curobj = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='suggested-city-PEZ']"
                ))
        )
        curobj.click()
        assert destination.get_attribute("value") == "Пенза", \
            "Ошибка: Поле 'Куда' заполнено некорректно"

    # Выбор даты
    with allure.step("Выбор даты поездки"):
        data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "button[data-test-id='start-date-field']"
                ))
        )
        data.click()
        curdata = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[aria-label='Tue Apr 01 2025']"
                ))
        )
        curdata.click()
        curdata.click()

    # Отправка формы поиска
    with allure.step("Отправка формы поиска"):
        ticket = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='form-submit']"
                ))
        )
        ticket.click()

    # Проверка корректности поля 'Откуда'
    with allure.step("Проверка корректности поля 'Откуда'"):

        assert origin.get_attribute("value") == "Москва", \
            "Ошибка: поле 'Откуда' заполнено некорректно."
        assert destination.get_attribute("value") == "Пенза", \
            "Ошибка: Поле 'Куда' заполнено некорректно"


@pytest.mark.ui
@allure.feature("Тестирование поиска авиабилетов")
@allure.story("Проверка ввода городов отправления и назначения")
@allure.title("Проверка корректного заполнения полей")
def test_ENGname(driver) -> str:
    # Ввод города отправления
    with allure.step("Ввод города отправления"):
        origin = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_origin-input"
                ))
        )
        origin.send_keys(Keys.CONTROL + "a")
        origin.send_keys(Keys.BACKSPACE)
        origin.send_keys("Moscow")

    # Ввод города назначения
    with allure.step("Ввод города назначения"):
        destination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_destination-input"
                ))
        )
        destination.click()
        DestInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='search-destination-input']"
                ))
        )
        DestInput.send_keys("Пенза")
        curobj = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='suggested-city-PEZ']"
                ))
        )
        curobj.click()
        assert destination.get_attribute("value") == "Пенза", \
            "Ошибка: Поле 'Куда' заполнено некорректно"

    # Выбор даты
    with allure.step("Выбор даты поездки"):
        data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "button[data-test-id='start-date-field']"
                ))
        )
        data.click()
        curdata = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[aria-label='Tue Apr 01 2025']"
                ))
        )
        curdata.click()
        curdata.click()

    # Отправка формы поиска
    with allure.step("Отправка формы поиска"):
        ticket = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='form-submit']"
                ))
        )
        ticket.click()

    # Проверка корректности поля 'Откуда'
    with allure.step("Проверка корректности поля 'Откуда'"):
        assert origin.get_attribute("value") == "Москва", \
            "Ошибка: поле 'Откуда' заполнено некорректно."


@allure.feature("Поиск авиабилетов")
@allure.story("Тестирование поля 'Откуда' и 'Куда'")
@pytest.mark.ui
@allure.title("Тест ввода имени с дефисом")
@allure.description("Данный тест проверяет корректность ввода данных в \
             форму поиска на сайте Aviasales с использованием дефиса.")
def test_name_is_2_world_dash(driverGOJ) -> str:
    with allure.step("Заполнение поля 'Откуда' с дефисом"):
        origin = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_origin-input"
                ))
        )
        origin.send_keys(Keys.CONTROL + "a")
        origin.send_keys(Keys.BACKSPACE)
        origin.send_keys("Нижний-новгород")

    with allure.step("Заполнение поля 'Куда'"):
        destination = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_destination-input"
                ))
        )
        destination.click()
        DestInput = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='search-destination-input']"
                ))
        )
        DestInput.send_keys("Пенза")
        curobj = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='suggested-city-PEZ']"
                ))
        )
        curobj.click()
        assert destination.get_attribute("value") == "Пенза", \
            "Ошибка: Поле 'Куда' заполнено некорректно"

    with allure.step("Выбор даты"):
        data = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "button[data-test-id='start-date-field']"
                ))
        )
        data.click()
        curdata = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[aria-label='Tue Apr 01 2025']"
                ))
        )
        curdata.click()
        curdata.click()

    with allure.step("Отправка формы поиска"):
        ticket = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='form-submit']"
                ))
        )
        ticket.click()

    with allure.step("Проверка корректности поля 'Откуда'"):
        assert origin.get_attribute("value") == "Нижний Новгород", \
            "Ошибка: поле 'Откуда' заполнено некорректно."


@allure.feature("Поиск авиабилетов")
@allure.story("Тестирование формы поиска")
@allure.title("Тест ввода названия из двух слов")
@allure.description("Данный тест проверяет корректность ввода \
                 данных в форму поиска на сайте Aviasales.")
def test_name_is_2_word_space(driverGOJ) -> str:
    with allure.step("Заполнение поля 'Откуда'"):
        origin = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_origin-input"
                ))
        )
        origin.send_keys(Keys.CONTROL + "a")
        origin.send_keys(Keys.BACKSPACE)
        origin.send_keys("Нижний Новгород")

    with allure.step("Заполнение поля 'Куда'"):
        destination = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_destination-input"
                ))
        )
        destination.click()
        DestInput = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='search-destination-input']"
                ))
        )
        DestInput.send_keys("Пенза")
        curobj = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='suggested-city-PEZ']"
                ))
        )
        curobj.click()
        assert destination.get_attribute("value") == "Пенза", \
            "Ошибка: Поле 'Куда' заполнено некорректно."

    with allure.step("Выбор даты"):
        data = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "button[data-test-id='start-date-field']"
                ))
        )
        data.click()
        curdata = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[aria-label='Tue Apr 01 2025']"
                ))
        )
        curdata.click()
        curdata.click()

    with allure.step("Отправка формы поиска"):
        ticket = WebDriverWait(driverGOJ, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='form-submit']"
                ))
        )
        ticket.click()

    with allure.step("Проверка коректности поля 'Откуда'"):
        assert origin.get_attribute("value") == "Нижний Новгород", \
            "Ошибка: поле 'Откуда' заполнено некорректно."


@allure.feature("Поиск авиабилетов")
@allure.story("Тестирование формы поиска")
@allure.title("Тест поиска авиабилетов")
@allure.description("Этот тест проверяет корректность ввода \
                 данных в форму поиска на сайте Aviasales.")
def test_search(driver) -> str:
    with allure.step("Заполнение поля 'Откуда'"):
        origin = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_origin-input"
                ))
        )
        origin.send_keys(Keys.CONTROL + "a")
        origin.send_keys(Keys.BACKSPACE)
        origin.send_keys("Москва")

    with allure.step("Заполнение поля 'Куда'"):
        destination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "#avia_form_destination-input"
                ))
        )
        destination.click()
        DestInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='search-destination-input']"
                ))
        )
        DestInput.send_keys("Пенза")
        curobj = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='suggested-city-PEZ']"
                ))
        )
        curobj.click()
        assert destination.get_attribute("value") == "Пенза", \
            "Ошибка: Поле 'Куда' заполнено некорректно."

    with allure.step("Выбор даты"):
        data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "button[data-test-id='start-date-field']"
                ))
        )
        data.click()
        curdata = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[aria-label='Tue Apr 01 2025']"
                ))
        )
        curdata.click()
        curdata.click()

    with allure.step("Отправка формы поиска"):
        ticket = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "[data-test-id='form-submit']"
                ))
        )
        ticket.click()

        assert origin.get_attribute("value") == "Москва", \
            "Ошибка: поле 'Откуда' заполнено некорректно."
