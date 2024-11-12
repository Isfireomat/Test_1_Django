from rest_framework import serializers
from .models import Link, Collection

class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class LinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    page_url = serializers.URLField()
    
    class Meta:
        model = Link
        fields = ['page_url']
    
    # def create(self, validated_data):
    #     link: Link = Link(
    #     title = 
    #     short_description = 
    #     link = validated_data['link']
    #     image = 
    #     type_url = )
    #     return link

class CollectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    description = serializers.CharField(required=False)

    class Meta:
        model = Collection
        fields = ['title', 'description']
        
    def create(self, validated_data):
        collection: Collection = Collection(**validated_data)
        return collection