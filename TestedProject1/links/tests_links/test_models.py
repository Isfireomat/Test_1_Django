import pytest
import binascii
from . import client, standart_user, standart_link, standart_collection
from links.models import Link, Collection
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_link_model(standart_link):
    link: Link = Link.objects.create(
        heading=standart_link['heading'],
        short_description=standart_link['short_description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url=standart_link['type_url']
    )
    assert link
    assert link.create_date_time
    assert link.change_date_time
    link: Link = Link.objects.create(
        heading=standart_link['heading'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url=standart_link['type_url']
    )
    assert link

@pytest.mark.django_db
def test_link_with_errors(standart_link):
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        heading='',
        short_description=standart_link['short_description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url=standart_link['type_url']
    )
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        heading=standart_link['heading'],
        short_description=standart_link['short_description'],
        page_url='tested',
        image=standart_link['image'],
        type_url=standart_link['type_url']
    )
    with pytest.raises(binascii.Error):
        link: Link = Link.objects.create(
        heading=standart_link['heading'],
        short_description=standart_link['short_description'],
        page_url=standart_link['page_url'],
        image='tested=',
        type_url=standart_link['type_url']
    )
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        heading=standart_link['heading'],
        short_description=standart_link['short_description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url='no website'
    )
    with pytest.raises(ValidationError):
        link: Link = Link.objects.create(
        short_description=standart_link['short_description'],
        page_url=standart_link['page_url'],
        image=standart_link['image'],
        type_url='no website'
    )

@pytest.mark.django_db
def test_collection_model(standart_collection):
    collection: Collection = Collection.objects.create(
        title=standart_collection['title'],
        short_description=standart_collection['short_description']
    )
    assert collection
    assert collection.create_date_time
    assert collection.change_date_time
    collection: Collection = Collection.objects.create(
        title=standart_collection['title'],
    )
    assert collection

@pytest.mark.django_db
def test_collection_model_with_errors(standart_collection):
    with pytest.raises(ValidationError):
        collection: Collection = Collection.objects.create(
            short_description=standart_collection['short_description'])
    