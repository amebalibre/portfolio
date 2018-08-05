"""Models of Blog."""
import datetime

from django.db import models
from django.utils import timezone

from .image import Image
from .tag import Tag


class Post(models.Model):
    """Post of Blog."""

    title = models.CharField(
        blank=False,
        max_length=200,
        null=False,
        unique=True,
    )
    content = models.CharField(max_length=1000)
    images = models.ManyToManyField(Image)
    pub_date = models.DateTimeField(
        'Date Published',
        default=datetime.date.today,
    )
    tags = models.ManyToManyField(Tag)

    def was_published(self):
        """If was published."""
        now = timezone.now()
        return self.pub_date <= now
    was_published.admin_order_field = 'pub_date'
    was_published.boolean = True
    was_published.short_description = 'Published recently?'

    def __str__(self):
        """Printable object."""
        return self.title

    class Meta:
        """Metadata."""

        ordering = (
            'pub_date',
            'title',
        )
