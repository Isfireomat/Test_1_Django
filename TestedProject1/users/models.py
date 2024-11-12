from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    email = models.EmailField(blank=False, null=False, unique=True)
    password = models.CharField(max_length=256, blank=False, null=False)
    create_date_time = models.DateTimeField(auto_now_add=True, null=False)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.password and not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def set_password(self, new_password: str):
        self.password = make_password(new_password)
        self.save()
    
    def __str__(self):
        return self.email
    