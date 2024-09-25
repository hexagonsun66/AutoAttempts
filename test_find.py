import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    """Инициализация веб-драйвера Chrome."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

def test_google_search(driver):
    """Тест на выполнение запроса в Google."""
    driver.get("https://www.google.com")

    # Находим поле ввода запроса и вводим текст запроса
    search_box = driver.find_element(By.NAME, "q")
    search_query = "Boards of Canada"
    search_box.send_keys(search_query + Keys.RETURN)

    # Ожидание появления результатов поиска
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))
    print(f"Запрос '{search_query}' выполнен, результаты поиска загружены.")
