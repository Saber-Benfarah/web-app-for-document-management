from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Archive
from django.forms import TextInput, Textarea
from django import forms

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'branch', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Info', {'fields': ('branch', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'branch', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Archive)
