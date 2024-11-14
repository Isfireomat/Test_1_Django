from typing import Optional, Union, Dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from users.utils import IsAuthenticatedWithToken
from links.utils import get_url_information
from links.models import Link, Collection
from links.serializers import LinkIdSerializer, CollectionIdSerializer,\
                         LinkSerializer, CollectionSerializer, \
                         LinkCollectionIdSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def create_link(request: Request) -> Response:
    serializer: LinkSerializer = LinkSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)  
    try:
        url_information: Dict[str, Optional[str]] = get_url_information(serializer.validated_data['page_url'])
        url_information.update({'user': request.user})
        Link.objects.create(**url_information)
    except Exception as e:
        return Response({'message':'link dont created', 
                         'Error': e}, 
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'link created'}, 
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def read_link(request: Request) -> Response:
    serializer: LinkIdSerializer = LinkIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    link: Link = Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                                     user=request.user)
    if not link: 
        return Response({'Error':'This linc is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'link': link.values().first()}, status=status.HTTP_200_OK)    

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def update_link(request: Request) -> Response:
    serializer: LinkSerializer = LinkSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not serializer.validated_data.get('user_link_id'):
        return Response({'message': 'user_link_id is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                               user=request.user).exists():
        return Response({'message': 'link is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        url_information: Dict[str, Optional[str]] = get_url_information(serializer.validated_data['page_url'])
        Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                            user=request.user).update(**url_information)
    except Exception as e:
        return Response({'message':'link dont update', 'Error': e}, 
                        status=status.HTTP_400_BAD_REQUEST)
    link: Link = Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                                     user=request.user)
    if not link:
        return Response({'Error':'This linc is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'link updated', 'link': link.values().first()}, 
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def delete_link(request: Request) -> Response:
    serializer: LinkIdSerializer = LinkIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                               user=request.user).exists():
        return Response({'Error':'This lincs is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    Link.objects.filter(user_link_id=serializer.validated_data['user_link_id'], 
                        user= request.user).delete() 
    return Response({'message': 'link deleted'}, 
                    status=status.HTTP_200_OK)  

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def create_collection(request: Request) -> Response:
    serializer: CollectionSerializer = CollectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)  
    Collection.objects.create(title=serializer.validated_data['title'],
                              description=serializer.validated_data['description'],
                              user=request.user)
    return Response({'message':'collection created'},
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def read_collection(request: Request) -> Response:
    serializer: CollectionSerializer = CollectionIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                     user=request.user).exists():
        return Response({'Error':'This collection is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    collection: Collection = Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                                       user=request.user)
    return Response({'collection': collection.values().first()}, 
                    status=status.HTTP_200_OK)    

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def update_collection(request: Request) -> Response:
    serializer: CollectionSerializer = CollectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not serializer.validated_data.get('user_collection_id'):
        return Response({'message': 'user_collection_id is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not  Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                      user=request.user).exists():
        return Response({'message': 'collection is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                  user=request.user).update(**serializer.validated_data)
    except Exception as e:
        return Response({'message':'collection dont update', 'Error': e}, 
                        status=status.HTTP_400_BAD_REQUEST)
    collection: Collection = Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                                       user=request.user)
    return Response({'message':'collection updated', 'collection': collection.values().first()}, 
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def delete_collection(request: Request) -> Response:
    serializer: CollectionIdSerializer = CollectionIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                     user=request.user).exists():
        return Response({'Error':'This collection is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                              user=request.user).delete() 
    return Response({'message': 'collection deleted'}, 
                    status=status.HTTP_200_OK) 

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def add_link_to_collection(request: Request) -> Response:
    serializer: LinkCollectionIdSerializer = LinkCollectionIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        link: Link = Link.objects.get(user_link_id=serializer.validated_data['user_link_id'],
                                    user=request.user)
    except Link.DoesNotExist:
        return Response({'message':'Incorect link'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    if not Collection.objects.filter(user_collection_id=serializer.validated_data['user_collection_id'], 
                                     user=request.user).exists():
        return Response({'Error':'This collection is not exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        Collection.objects.get(user_collection_id=serializer.validated_data['user_collection_id'], 
                                user=request.user).links.add(link)
    except Exception as e:
        return Response({'message':'collection dont update', 'Error': e}, 
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'link add to collection'}, 
                    status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticatedWithToken])
def read_links_from_collection(request: Request) -> Response:
    serializer: CollectionIdSerializer = CollectionIdSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        collection: Collection = Collection.objects.get(
            user_collection_id=serializer.validated_data['user_collection_id'],
            user=request.user)
    except Collection.DoesNotExist:
        return Response({'Error':'Incorect collection'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'links':list(collection.links.all().values())},
                    status=status.HTTP_200_OK)