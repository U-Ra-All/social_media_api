from django.contrib import admin
from django.contrib.auth.models import Group

from posts.models import Post, Like, Comment

admin.site.unregister(Group)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
