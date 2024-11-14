from typing import Dict, Union
from links.serializers import LinkIdSerializer, CollectionIdSerializer, \
                              LinkSerializer, CollectionSerializer

def test_link_id_serializer() -> None:
    data: Dict[str, int] = {'user_link_id':1}
    serializer: LinkIdSerializer = LinkIdSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'user_link_id':'1'}
    serializer: LinkIdSerializer = LinkIdSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, int] = {'email':1}
    serializer: LinkIdSerializer = LinkIdSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, str] = {'user_link_id':'e'}
    serializer: LinkIdSerializer = LinkIdSerializer(data=data)
    assert not serializer.is_valid()

def test_collection_id_serializer() -> None:
    data: Dict[str, int] = {'user_collection_id':1}
    serializer: CollectionIdSerializer = CollectionIdSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'user_collection_id':'1'}
    serializer: CollectionIdSerializer = CollectionIdSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, int] = {'email':1}
    serializer: CollectionIdSerializer = CollectionIdSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, str] = {'user_collection_id':'e'}
    serializer: CollectionIdSerializer = CollectionIdSerializer(data=data)
    assert not serializer.is_valid()

def test_link_serializer() -> None:
    data: Dict[str, Union[str, int]] = {'user_link_id':1, 
                                        'page_url':'https://thelastgame.ru/dwarf-fortress/'}
    serializer: LinkSerializer = LinkSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'page_url':'https://thelastgame.ru/dwarf-fortress/'}
    serializer: LinkSerializer = LinkSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'url':'https://thelastgame.ru/dwarf-fortress/'}
    serializer: LinkSerializer = LinkSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, int] = {'user_link_id':1}
    serializer: LinkSerializer = LinkSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, str] = {'page_url':'thelastgame.ru/dwarf-fortress/'}
    serializer: LinkSerializer = LinkSerializer(data=data)
    assert not serializer.is_valid()
    
def test_collection_serializer() -> None:
    data: Dict[str, Union[str, int]]= {
            'user_collection_id': 1, 
            'title': 'test', 
            'description': 'test_descriptions'
            }
    serializer: CollectionSerializer = CollectionSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'title':'test'}
    serializer: CollectionSerializer = CollectionSerializer(data=data)
    assert serializer.is_valid()
    data: Dict[str, str] = {'test':'test'}
    serializer: CollectionSerializer = CollectionSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, int] = {'user_collection_id':1}
    serializer: CollectionSerializer = CollectionSerializer(data=data)
    assert not serializer.is_valid()
    data: Dict[str, str] = {'description':'test_description'}
    serializer: CollectionSerializer = CollectionSerializer(data=data)
    assert not serializer.is_valid()