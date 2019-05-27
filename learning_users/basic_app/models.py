from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfoForm(models.Model):
    # this is for adding more atributes from the User model, using one to one field not inchereting, because it can mess up the DB
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # declaring the additional classes for the User (default: username, password..)
    # blank=True --> user may not have any portfolio, optional field
    portfolio_site = models.URLField(blank=True)

    # user can upload profile pic (upload_to whihc is sub dir of media folder) or maybe not (blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    # method for printing out the information of the models
    def __str__(self):
        return self.user.username
