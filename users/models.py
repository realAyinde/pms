from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_doctor = models.BooleanField(default=False)
    mobile_phone = models.CharField(blank=True, max_length=20)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default="Male")
    

    def __str__(self):
        return "{} @ {}".format(self.get_full_name(), self.email)

    def get_full_name(self):
        return self.first_name +' '+ self.last_name
    
