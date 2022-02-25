from django.db import models

# Create your models here.
class Users(models.Model):

    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)


class Book(models.Model):

    name = models.CharField(max_length=30)
    price = models.FloatField()
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    abstract = models.TextField()
    img_url = models.CharField(max_length=150)
    pub_date = models.DateField()