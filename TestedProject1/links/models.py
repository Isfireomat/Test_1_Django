from django.db import models

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
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Collection(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=500, blank=True)
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    change_date_time = models.DateTimeField(auto_now=True, null=False)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
