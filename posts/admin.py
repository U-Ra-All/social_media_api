from django.contrib import admin
from django.contrib.auth.models import Group

from posts.models import Post

admin.site.unregister(Group)
admin.site.register(Post)
