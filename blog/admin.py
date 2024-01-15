from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    readonly_fields =("created", )

# Register your models here.
admin.site.register(Blog, BlogAdmin)
