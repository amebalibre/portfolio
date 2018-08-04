"""Models of Blog."""
import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    """Keyword assigned to a post."""

    name = models.CharField(
        blank=False,
        max_length=30,
        null=False,
        unique=True,
        )
    color = models.CharField(
        default='#3F7C82',
        max_length=7,
        validators=[RegexValidator(
            regex='^#.{6}$',
            message='Char has to be Hash key and a Hexadecimal code with 6 '
                    'char lenght. Example: #FFFFFF (one hash and 6 chars)',
            code='nomatch'
        )]
    )

    def check_color_format(self):
        """Check long and hexa code of color.

        Correct format requires seven characters. First '#' and six hex chars.
        """
        try:
            if(self.color and len(self.color) == 7 and self.color[0] == '#'):
                int(self.color[1:], 16)
                return True
        except ValueError:
            pass
        return False

    def __str__(self):
        """Printable object."""
        return self.name

    class Meta:
        """Metadata."""

        ordering = (
            'name',
        )


class Image(models.Model):
    """Images of posts."""

    name = models.CharField(
        max_length=15,
        null=False,
        unique=True,
    )
    image = models.ImageField()

    def __str__(self):
        """Printable object."""
        return self.name

    class Meta:
        """Metadata."""

        ordering = (
            'name',
        )


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
