from django.contrib import admin
from golf.managers import CustomUserManager
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import Getnewsletter, Contact_us, Events
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

class Getnewsletter(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Get newsletters"


class Contact_us(models.Model):
    full_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    comments = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact us"
        ordering = ('-created_a',)


class Events(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)
    caption = models.TextField()
    data = models.DateField()
    location = models.CharField(max_length=255)
    ticket = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ('-created_at',)


class CustomImportExportModelAdmin(ImportExportModelAdmin):
    def get_import_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

class GetnewsletterAdmin(CustomImportExportModelAdmin):
    resource_class = Getnewsletter

class Contact_usAdmin(CustomImportExportModelAdmin):
    resource_class = Contact_us

class EventsAdmin(CustomImportExportModelAdmin):
    resource_class = Events

admin.site.register(Getnewsletter, GetnewsletterAdmin)
admin.site.register(Contact_us, Contact_usAdmin)
admin.site.register(Events, EventsAdmin)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
