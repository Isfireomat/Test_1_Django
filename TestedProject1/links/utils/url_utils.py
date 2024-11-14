import requests
from typing import Optional, List, Dict
from rest_framework.response import Response
from bs4 import BeautifulSoup
from bs4.element import Tag
from links.models import Link

TYPE_URL_CHOICES: List[str]  = [i[0] for i in Link.TYPE_URL_CHOICES]
    
def get_url_information(url: str) -> Dict[str, Optional[str]]:
    response: Response = requests.get(url)
    if response.status_code != 200: 
        raise requests.exceptions.HTTPError('Error with load page')
    information: Dict[str, Optional[str]] = {
        'title': None,
        'description': None,
        'page_url': url,
        'image': None,
        'type_url': 'website'
    }
    soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
    meta_tags: List[Tag] = soup.find_all('meta',  attrs={'name': True})
    data: Dict[str, str] = {tag['name']: tag['content'] \
                            for tag in meta_tags if tag.get('content')}
    title_tag: Optional[Tag] = soup.find('title')
    data.update({'title': title_tag.string if title_tag else None})
    og_meta_tags: List[Tag] = soup.find_all('meta', 
                                            property=lambda x: x and x.startswith('og:'))
    og_data: Dict[str, str] = {tag['property'].replace('og:',''): tag['content'] \
                               for tag in og_meta_tags if tag.get('content')}
    for key in information.keys():
        information[key] = og_data.get(key, data.get(key, information[key]))
    information['type_url'] = information['type_url'] \
                              if information['type_url'] in TYPE_URL_CHOICES \
                              else 'website'
    return information