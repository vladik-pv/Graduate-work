import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


@allure.feature("Поиск авиабилетов")
@allure.story("Тестирование формы поиска")
@pytest.fixture(scope="module")
def driver():
    with allure.step("Инициализация драйвера и открытие страницы сайта"):
        driver = webdriver.Chrome()
        driver.get("https://www.aviasales.ru/?params=MOW1")
        yield driver
        driver.quit()


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
