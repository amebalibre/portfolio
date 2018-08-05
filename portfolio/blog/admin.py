from django.contrib import admin

from .models.post import Post
from .models.image import Image
from .models.tag import Tag

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Tag)
