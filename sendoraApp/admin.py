from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from sendoraApp import models
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class CustomAdminClass(UserAdmin, ModelAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    # change_password_form = AdminPasswordChangeForm
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active', 'last_login', ]
