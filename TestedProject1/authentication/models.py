from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
class User(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=256, blank=False, null=False)
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    
    def validate(self):
        if not self.email:
            raise ValidationError("Email is required")
        if not self.password:
            raise ValidationError("Password is required")

    def save(self, *args, **kwargs):
        self.validate()
        if self.password and not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def set_password(self, new_password: str):
        self.password = make_password(new_password)
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
    