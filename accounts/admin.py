from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_display= ['id', 'last_name', 'email', 'first_name', 'roles']
    list_filter = ['roles']
    search_fields = ["email"]
    ordering = ["email" , "id"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display= ['user', 'name', 'phone_number']
    list_filter = ['age', 'gender', ]
    search_fields = ["email"]
    # ordering = ["email" , "id"]
    show_facets = admin.ShowFacets.ALWAYS
