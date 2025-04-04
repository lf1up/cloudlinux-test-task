from django.db import models

from django.apps import apps
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import pre_save
from django.core.validators import EmailValidator
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
    UnicodeUsernameValidator,
)
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class County(models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=60)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        if username is not None:
            username = GlobalUserModel.normalize_username(username)

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, username=None, **extra_fields):
        return self._create_user(
            email, password, username, is_staff=True, is_superuser=True, **extra_fields
        )


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[email_validator],
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_("150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)  # for possibility to deactivate user

    gender = models.CharField(max_length=150, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(pre_save, sender=User)
def give_default_username(sender, instance, *args, **kwargs):
    if not instance.first_name:
        instance.first_name = ""
    if not instance.last_name:
        instance.last_name = ""
