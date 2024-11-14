from rest_framework import serializers
from .models import Link, Collection

class LinkCollectionIdSerializer(serializers.Serializer):
    user_link_id = serializers.IntegerField()
    user_collection_id = serializers.IntegerField()

class LinkIdSerializer(serializers.Serializer):
    user_link_id = serializers.IntegerField()

class CollectionIdSerializer(serializers.Serializer):
    user_collection_id = serializers.IntegerField()

class LinkSerializer(serializers.ModelSerializer):
    user_link_id = serializers.IntegerField(required=False)
    page_url = serializers.URLField()
    
    class Meta:
        model = Link
        fields = ['user_link_id','page_url']


class CollectionSerializer(serializers.ModelSerializer):
    user_collection_id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    description = serializers.CharField(required=False)

    class Meta:
        model = Collection
        fields = ['user_collection_id','title', 'description']
        
    def create(self, validated_data):
        collection: Collection = Collection(**validated_data)
        return collection