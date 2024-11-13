from . import standart_link
from links.serializers import LinkIdSerializer, CollectionIdSerializer, \
                              LinkSerializer, CollectionSerializer

def test_link_id_serializer():
    data = {'user_link_id':1}
    serializer = LinkIdSerializer(data=data)
    assert serializer.is_valid()
    data = {'user_link_id':'1'}
    serializer = LinkIdSerializer(data=data)
    assert serializer.is_valid()
    data = {'email':1}
    serializer = LinkIdSerializer(data=data)
    assert not serializer.is_valid()
    data = {'user_link_id':'e'}
    serializer = LinkIdSerializer(data=data)
    assert not serializer.is_valid()

def test_collection_id_serializer():
    data = {'user_collection_id':1}
    serializer = CollectionIdSerializer(data=data)
    assert serializer.is_valid()
    data = {'user_collection_id':'1'}
    serializer = CollectionIdSerializer(data=data)
    assert serializer.is_valid()
    data = {'email':1}
    serializer = CollectionIdSerializer(data=data)
    assert not serializer.is_valid()
    data = {'user_collection_id':'e'}
    serializer = CollectionIdSerializer(data=data)
    assert not serializer.is_valid()

def test_link_serializer():
    data = {'user_link_id':1, 'page_url':'https://thelastgame.ru/dwarf-fortress/'}
    serializer = LinkSerializer(data=data)
    assert serializer.is_valid()
    data = {'page_url':'https://thelastgame.ru/dwarf-fortress/'}
    serializer = LinkSerializer(data=data)
    assert serializer.is_valid()
    data = {'url':'https://thelastgame.ru/dwarf-fortress/'}
    serializer = LinkSerializer(data=data)
    assert not serializer.is_valid()
    data = {'user_link_id':1}
    serializer = LinkSerializer(data=data)
    assert not serializer.is_valid()
    data = {'page_url':'thelastgame.ru/dwarf-fortress/'}
    serializer = LinkSerializer(data=data)
    assert not serializer.is_valid()
    
def test_collection_serializer():
    data = {'user_collection_id': 1, 
            'title': 'test', 
            'description': 'test_descriptions'}
    serializer = CollectionSerializer(data=data)
    assert serializer.is_valid()
    data = {'title':'test'}
    serializer = CollectionSerializer(data=data)
    assert serializer.is_valid()
    data = {'test':'test'}
    serializer = CollectionSerializer(data=data)
    assert not serializer.is_valid()
    data = {'user_collection_id':1}
    serializer = CollectionSerializer(data=data)
    assert not serializer.is_valid()
    data = {'description':'test_description'}
    serializer = CollectionSerializer(data=data)
    assert not serializer.is_valid()