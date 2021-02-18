from django.contrib import admin
from .models import Like, User, articles, spheres, comments
from pagedown.widgets import AdminPagedownWidget
from django.db import models

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author','topic', 'status')
    list_filter = ('status',)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

admin.site.register(User)
admin.site.register(comments)
admin.site.register(spheres)
admin.site.register(articles, ArticleAdmin)
admin.site.register(Like)