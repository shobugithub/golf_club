from django.contrib import admin
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import MyModel
# Register your models here.

from . import models

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('account/', include('account.urls')),
#     path('social-auth/',
#     include('social_django.urls', namespace='social')),
# ]

admin.site.register(models.Contact_us)
admin.site.register(models.Events)
admin.site.register(models.Getnewsletter)

class MyModelResource(resources.ModelResource):
    class Meta:
        model = MyModel
        fields = ('id', 'name', 'description')

class MyModelAdmin(ImportExportModelAdmin):
    resource_class = MyModelResource

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

admin.site.register(MyModel, MyModelAdmin)
