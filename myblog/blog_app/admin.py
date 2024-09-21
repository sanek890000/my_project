from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'views')
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
