from django.contrib import admin

# Register your models here.
from .models import  User, Blotter

# admin.site.register(User)
admin.site.register(Blotter)
admin.site.register(User)

