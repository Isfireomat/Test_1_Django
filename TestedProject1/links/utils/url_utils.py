import requests
from bs4 import BeautifulSoup
from links.models import Link

TYPE_URL_CHOICES = [i[0] for i in Link.TYPE_URL_CHOICES]
    
def get_url_information(url: str):
    response = requests.get(url)
    if response.status_code != 200: 
        raise requests.exceptions.HTTPError('Error with load page')
    information = {
        'title': None,
        'description': None,
        'url': url,
        'image': None,
        'type': 'website'
    }
    soup = BeautifulSoup(response.text, 'html.parser')
    no_og_meta_tags = soup.find_all('meta',  attrs={'name': True})
    no_og_data = {tag["name"]: tag["content"] for tag in no_og_meta_tags if tag.get("content")}
    no_og_data.update({'title':soup.find('title').string})
    og_meta_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
    og_data = {tag["property"].replace('og:',''): tag["content"] for tag in og_meta_tags if tag.get("content")}
    for key in information.keys():
        information[key] = og_data.get(key, no_og_data.get(key, information[key]))
    information['type'] = information['type'] if information['type'] in TYPE_URL_CHOICES else 'website'
    return information