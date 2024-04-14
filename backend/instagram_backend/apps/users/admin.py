from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User  # Assuming you're using Django's default User model


class CustomUserAdmin(BaseUserAdmin):
    filter_horizontal = ('groups', 'user_permissions')  # Add this line to include 'groups' and 'user_permissions'
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff')  # Add this line to include 'first_name', 'last_name', and 'is_staff'
    list_filter = ('is_staff', 'is_superuser', 'is_active',
                   'groups')  # Add this line to include 'is_staff', 'is_superuser', 'is_active', and 'groups'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
