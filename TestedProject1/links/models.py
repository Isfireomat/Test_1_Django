from typing import List, Tuple
from django.db import models
from users.models import User

class Link(models.Model):
    TYPE_URL_CHOICES: List[Tuple[str, str]] = [
    ('website', 'Website'),
    ('book', 'Book'),
    ('article', 'Article'),
    ('music', 'Music'),
    ('video', 'Video'),]
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(blank=True)
    page_url = models.URLField(blank=False, null=False)
    image = models.URLField(blank=True,  null=True)
    type_url = models.CharField(max_length=50 ,choices=TYPE_URL_CHOICES, default='website')
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='links',
        blank=False
        )
    user_link_id = models.PositiveIntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'page_url'], name='unique_user_page_url'),
            models.UniqueConstraint(fields=['user', 'user_link_id'], name='unique_user_link')
        ]
    
    def save(self, *args, **kwargs) -> None:
        if not self.user_link_id:
            last_id = Link.objects.filter(user=self.user).aggregate(models.Max('user_link_id'))['user_link_id__max'] or 0   
            self.user_link_id = last_id + 1
        self.full_clean()
        super().save(*args, **kwargs)

class Collection(models.Model):
    title = models.CharField(blank=False, null=False)
    description = models.CharField(blank=True)
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
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_user_collection_title'),
            models.UniqueConstraint(fields=['user', 'user_collection_id'], name='unique_user_collection')
        ]
    
    def save(self, *args, **kwargs) -> None:
        if not self.user_collection_id:
            last_id = Collection.objects.filter(user=self.user).aggregate(models.Max('user_collection_id'))['user_collection_id__max'] or 0
            self.user_collection_id = last_id + 1
        self.full_clean()
        super().save(*args, **kwargs)
