from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Company

class company(admin.ModelAdmin):
    list_display = ["useres", "cnpj", "address"]
    

admin.site.register(Company, ModelAdmin)
