from django.contrib import admin

from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    exclude = ('user', 'content', 'gdoc_link', 'landing_page', 'status', 'reject_message')


admin.site.register(Blog, BlogAdmin)
