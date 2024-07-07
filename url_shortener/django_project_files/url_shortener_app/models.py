from django.db import models

# Create your models here.

class Urls(models.Model):
    url = models.TextField()
    hashed_url = models.TextField()
    website_name = models.TextField()
    username = models.TextField()