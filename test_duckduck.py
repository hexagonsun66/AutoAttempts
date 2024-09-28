import requests
from bs4 import BeautifulSoup
import pytest

def test_duckduck():
    url = 'https://duckduckgo.com/html/?q=Radiohead'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    response = requests.get(url, headers=headers)

    # Проверяем, что запрос успешен
    assert response.status_code == 200, "Статус запроса должен быть 200 (успешный)"

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем все ссылки на результаты поиска
    links = []
    for item in soup.find_all('a', {'class': 'result__a'}):
        link = item.get('href')
        if link:
            links.append(link)

    # Проверяем, что мы нашли хотя бы одну ссылку
    assert len(links) > 0, "Должна быть хотя бы одна ссылка в результатах поиска"

    # Печатаем найденные ссылки
    print("Найденные ссылки:")
    for link in links[:5]:  # Выводим первые 5 ссылок
        print(link)

