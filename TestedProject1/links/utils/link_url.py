import requests
from bs4 import BeautifulSoup

def get_url_information(url: str):
    response = requests.get(url)
    if response.status_code != 200: 
        raise requests.exceptions.HTTPError('Error with load page')
    information = {
        'title': None,
        'description': None,
        'page_url': None,
        'image': None,
        'type_url': 'website'
    }
    soup = BeautifulSoup(response.text, 'html.parser')
   
    og_meta_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
    og_data = {tag["property"]: tag["content"] for tag in og_meta_tags if tag.get("content")}

# - заголовок страницы;   
# - краткое описание;   
# - ссылка на страницу;   
# - картинка;   
# - тип ссылки (website, book, article, music, video). Если не удалось получить тип страницы то по умолчанию используем тип website. Картинка превью берется из поля og:image.   

# <meta property="og:title" content="Заголовок страницы" />
# <meta property="og:description" content="Описание страницы" />
# <meta property="og:image" content="https://example.com/image.jpg" />
# <meta property="og:url" content="https://example.com/page" />