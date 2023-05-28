from django.contrib import admin
from django.contrib.auth.models import Group

from posts.models import Post, Like

admin.site.unregister(Group)
admin.site.register(Post)
admin.site.register(Like)
