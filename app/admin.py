from django.contrib import admin
from .models import Profile, Tag, Post, Comment, Subscribe, WebsiteMeta
# Register your models here.


admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Subscribe)
admin.site.register(WebsiteMeta)
