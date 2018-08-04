from django.contrib import admin

from .models import Post
from .models import Image
from .models import Tag

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Tag)
