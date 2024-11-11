from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    hashed_password = models.CharField(max_length=50, blank=False, null=False)
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    
    def save(self, *args, **kwargs):
        if self.hashed_password and not self.pk:
            self.hashed_password = make_password(self.hashed_password)
        super().save(*args, **kwargs)

    def set_password(self, new_password: str):
        self.hashed_password = make_password(new_password)
        self.save() 
        
class Link(models.Model):
    TYPE_URL_CHOICES = [
    ("website", "Website"),
    ("book", "Book"),
    ("article", "Article"),
    ("music", "Music"),
    ("video", "Video"),]
    heading = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=500, blank=True)
    page_url = models.URLField(blank=False, null=False)
    image = models.BinaryField(blank=True,  null=True)
    type_url = models.CharField(max_length=100 ,choices=TYPE_URL_CHOICES, default="website")
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    
class Collection(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=500, blank=True)
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    