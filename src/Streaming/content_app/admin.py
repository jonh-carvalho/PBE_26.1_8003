from django.contrib import admin
from content_app.models import Comment, Content

# Register your models here.
admin.site.register(Content)
admin.site.register(Comment)