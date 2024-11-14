from django.urls import path
from .views import create_link, create_collection, \
                   read_link, read_collection, \
                   update_link, update_collection, \
                   delete_link, delete_collection, \
                   add_link_to_collection, read_links_from_collection
urlpatterns = [
   path('create_link/', create_link, name='create_link'),
   path('read_link/', read_link, name='read_link'),
   path('update_link/', update_link, name='update_link'),
   path('delete_link/', delete_link, name='delete_link'),
   path('create_collection/', create_collection, name='create_collection'),
   path('read_collection/', read_collection, name='read_collection'),
   path('update_collection/', update_collection, name='update_collection'),
   path('delete_collection/', delete_collection, name='delete_collection'),
   path('add_link_to_collection/', add_link_to_collection, name='add_link_to_collection'),
   path('read_links_from_collection/', read_links_from_collection, name='read_links_from_collection'),
]