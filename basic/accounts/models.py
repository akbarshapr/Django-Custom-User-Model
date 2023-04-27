import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


def validate_age(date_of_birth):
    today = datetime.date.today()
    age = today.year - date_of_birth.year - \
        ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    if age < 18:
        raise ValidationError(_('You must be 18 years or older to register.'))


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=20, validators=[MinLengthValidator(3)])
    email = models.EmailField(unique=True)
    phone = models.IntegerField(blank=True, null=True, validators=[
        RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')
    ])
    date_of_birth = models.DateField(validators=[validate_age])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'date_of_birth']

    objects = CustomUserManager()
