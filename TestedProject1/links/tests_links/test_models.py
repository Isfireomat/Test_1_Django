import pytest
import binascii
from . import client, standart_user, \
              standart_link, standart_collection, \
              registration, user
from links.models import Link, Collection
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_link_model(standart_link, user):
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
    link: Link = Link.objects.create(
        title=standart_link['title'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url=standart_link['type_url'],
        user=user 
    )
    assert link

@pytest.mark.django_db
def test_link_with_errors(standart_link, user):
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
    with pytest.raises(binascii.Error):
        link: Link = Link.objects.create(
        title=standart_link['title'],
        description=standart_link['description'],
        page_url=standart_link['page_url'],
        image='tested=',
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
def test_collection_model(standart_collection, user):
    collection: Collection = Collection.objects.create(
        title=standart_collection['title'],
        description=standart_collection['description'],
        user=user 
    )
    assert collection
    assert collection.create_date_time
    assert collection.change_date_time
    collection: Collection = Collection.objects.create(
        title=standart_collection['title'],
        user=user 
    )
    assert collection

@pytest.mark.django_db
def test_collection_model_with_errors(standart_collection, user):
    with pytest.raises(ValidationError):
        collection: Collection = Collection.objects.create(
            description=standart_collection['description'],
            user=user)
    