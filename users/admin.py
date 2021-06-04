from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'is_doctor')}),
        ('Contact info', {'fields': ('email', 'mobile_phone')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Login Info', {'fields': ('username', 'password')}),
    )
    list_display = ['email', 'username', 'is_doctor']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_doctor',)


admin.site.register(User, UserAdmin)
