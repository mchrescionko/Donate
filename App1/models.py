import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)

TYPE = (
    (1,"fundacja"),
    (2,"organizacja pozarządowa"),
    (3,"zbiórka lokalna"),
)

class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE, default=1)
    category = models.ManyToManyField(Category)

class User(AbstractUser):
    tokenResetPassword = models.UUIDField(null=True, unique=True)
    class Meta:
        db_table = 'auth_user'

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

