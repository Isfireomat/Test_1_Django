from typing import Dict
from django.core.exceptions import ValidationError
import pytest
from users.models import User
from links.models import Link, Collection
from conftest import standart_user, standart_link, registration, \
                     standart_collection, user

@pytest.mark.django_db
def test_link_model(standart_link: Dict[str, str], 
                    user: User) -> None:
    link: Link = Link.objects.create(
        title=standart_link['title'],
        description=standart_link['description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url=standart_link['type_url'],
        user=user 
    )
    assert link
    assert link.create_date_time
    assert link.change_date_time
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        title='',
        description=standart_link['description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url=standart_link['type_url'],
        user=user 
    )
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        title=standart_link['title'],
        description=standart_link['description'],
        page_url='tested',
        image=standart_link['image'],
        type_url=standart_link['type_url'],
        user=user 
    )
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        title=standart_link['title'],
        description=standart_link['description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url='no website',
        user=user 
    )
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        description=standart_link['description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url='no website',
        user=user 
    )

@pytest.mark.django_db
def test_collection_model(standart_collection: Dict[str, str], 
                          user: User) -> None:
    collection: Collection = Collection.objects.create(
        title=standart_collection['title'],
        description=standart_collection['description'],
        user=user 
    )
    assert collection
    assert collection.create_date_time
    assert collection.change_date_time
    collection: Collection = Collection.objects.create(
        title='tested title',
        user=user 
    )
    assert collection
    with pytest.raises(ValidationError):
        collection: Collection = Collection.objects.create(
            description=standart_collection['description'],
            user=user)
    