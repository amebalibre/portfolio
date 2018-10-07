"""Models of Blog."""
from django.conf import settings
from django.db import models
from django.utils import timezone

from .image import Image
from .tag import Tag

import alu_configparser as alu_cp


class Post(models.Model):
    """Post of Blog."""

    title = models.CharField(
        blank=False,
        max_length=200,
        null=False,
        unique=True,
    )
    content = models.TextField(max_length=1000)
    images = models.ManyToManyField(Image)
    pub_date = models.DateTimeField(
        'Date Published',
        auto_now_add=True,
    )
    tags = models.ManyToManyField(Tag)

    def was_published(self):
        """If was published."""
        now = timezone.now()
        return self.pub_date <= now
    was_published.admin_order_field = 'pub_date'
    was_published.boolean = True
    was_published.short_description = 'Published recently?'

    @property
    def short_content(self):
        """Return a fraction of the content."""
        config = alu_cp.Configparser(
            path=settings.ENVIRONMENT['development'],
            fname=settings.FILECONFIG,
        ).get()
        _from = config.getint('portfolio.blog', 'short_content')
        _to = self.content[:_from].rfind(' ')
        return '{content}{excess}'.format(
            content=self.content[:_to],
            excess='...' if self.content[_from:] else ''
        )

    def __str__(self):
        """Printable object."""
        return self.title

    class Meta:
        """Metadata."""

        ordering = (
            'pub_date',
            'title',
        )
