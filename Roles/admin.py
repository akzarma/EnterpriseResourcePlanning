from django.contrib import admin

# Register your models here.
# from django.contrib.auth.admin import UserAdmin
from .models import  RoleMaster, RoleManager

admin.site.register(RoleMaster)
admin.site.register(RoleManager)
