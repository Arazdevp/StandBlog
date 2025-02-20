from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100)
    national_code = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profiles/images', blank=True, null=True)

    def __str__(self):
        return self.user.username