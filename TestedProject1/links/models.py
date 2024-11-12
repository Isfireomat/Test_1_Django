from django.db import models
from users.models import User
class Link(models.Model):
    TYPE_URL_CHOICES = [
    ("website", "Website"),
    ("book", "Book"),
    ("article", "Article"),
    ("music", "Music"),
    ("video", "Video"),]
    heading = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=500, blank=True)
    link = models.URLField(blank=False, null=False)
    image = models.BinaryField(blank=True,  null=True)
    type_url = models.CharField(max_length=100 ,choices=TYPE_URL_CHOICES, default="website")
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='links')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Collection(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=500, blank=True)
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections')
    links = models.ManyToManyField(
        Link,
        related_name='links')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
