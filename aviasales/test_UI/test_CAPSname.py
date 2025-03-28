import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    # Открытие браузера и переход на сайт
    driver = webdriver.Chrome()
    driver.get("https://www.aviasales.ru/?params=MOW1")
    yield driver
    driver.quit()


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
