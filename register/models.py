from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework.authtoken.models import Token

from .managers import UserManager
from .validators import validate_CPF

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def upload_file_customer(instance, filename):
    return f"{instance.name}-{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(
        _("first name"), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    cpf = models.CharField(
        "CPF",
        unique=True,
        max_length=14,
        validators=[validate_CPF],
        blank=True,
        null=True,
    )
    document = models.FileField(upload_to="meusarquivos", blank=False, null=True)
    address = models.CharField(max_length=90, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    company_id = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Client(User):
    class Meta:
        proxy = True
        verbose_name = "Client"

        verbose_name_plural = "Clients"


#    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
#    def create_auth_token(sender, instance=None, created=False, **kwargs):
#        if created:
#            Token.objects.create(user=instance)
#
#    pass
