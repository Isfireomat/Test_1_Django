from typing import List, Tuple
from django.db import models
from users.models import User

class Link(models.Model):
    TYPE_URL_CHOICES: List[Tuple[str]] = [
    ('website', 'Website'),
    ('book', 'Book'),
    ('article', 'Article'),
    ('music', 'Music'),
    ('video', 'Video'),]
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=2000, blank=True)
    page_url = models.URLField(blank=False, null=False)
    image = models.CharField(max_length=500, blank=True,  null=True)
    type_url = models.CharField(max_length=100 ,choices=TYPE_URL_CHOICES, default='website')
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='links',
        blank=False
        )
    user_link_id = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs) -> None:
        if not self.user_link_id:
            last_link: Link = Link.objects.filter(user=self.user).order_by('user_link_id').last()
            self.user_link_id: int = last_link.user_link_id + 1 if last_link else 1
        self.full_clean()
        super().save(*args, **kwargs)

class Collection(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=2000, blank=True)
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections',
        blank=False
        )
    links = models.ManyToManyField(
        Link,
        related_name='links',
        blank=True
        )
    user_collection_id = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs) -> None:
        if not self.user_collection_id:
            last_collection: Collection = Collection.objects.filter(user=self.user).order_by('user_collection_id').last()
            self.user_collection_id: int = last_collection.user_collection_id + 1 if last_collection else 1
        self.full_clean()
        super().save(*args, **kwargs)
