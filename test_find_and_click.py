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
    # Инициализация веб-драйвера с автоматическим управлением драйвером
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Закрытие браузера после завершения теста
    driver.quit()


def test_google_search(driver):
    # Открытие Google
    driver.get("https://www.google.com")

    # Поиск элемента поля ввода поиска
    search_box = driver.find_element(By.NAME, "q")

    # Ввод запроса и нажатие Enter
    search_query = "Swans"
    search_box.send_keys(search_query + Keys.RETURN)

    # Явное ожидание загрузки результатов поиска
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))

    # Поиск всех ссылок, содержащих заголовки результатов поиска
    search_results = driver.find_elements(By.CSS_SELECTOR, 'a h3')

    # Ищем первую кликабельную ссылку из реальных результатов поиска
    first_valid_link = None
    for result in search_results:
        parent_link = result.find_element(By.XPATH, './ancestor::a')
        href = parent_link.get_attribute('href')
        if href and "http" in href:
            first_valid_link = parent_link
            break

    # Если найдена первая ссылка, выполняем клик через JavaScript
    if first_valid_link:
        driver.execute_script("arguments[0].scrollIntoView();", first_valid_link)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(first_valid_link))

        # Клик с помощью JavaScript
        driver.execute_script("arguments[0].click();", first_valid_link)

        # Дополнительные действия на новой странице
        assert driver.current_url != "https://www.google.com", "Не удалось перейти на первую ссылку"
        print("Успешно перешли на первую ссылку")
    else:
        pytest.fail("Не удалось найти подходящую ссылку для перехода.")