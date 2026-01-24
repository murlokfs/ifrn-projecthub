from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'role')
    search_fields = ('username', 'email', 'full_name', 'registration')
    list_filter = ('role',)
    
admin.site.register(User, UserAdmin)


# Register your models here.
