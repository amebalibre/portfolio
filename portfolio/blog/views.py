"""All Views."""
from django.views import generic

from .models.post import Post
from .models.post import Tag


class IndexView(generic.ListView):
    """Landspage view.

    Shows latest six published posts. Post is published when pub_date is lower
    to today
    """

    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the last six published posts."""
        return Post.objects.order_by('-pub_date')[:6]


class FilterTagView(generic.ListView):
    """Landspage filtered view from tags.

    Shows posts with tags coincidence.
    """

    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the last six published posts."""
        return Post.objects.filter(
            tags__in=Tag.objects.filter(
                name=self.kwargs['tag']
            ).values('id')
        )


class DetailView(generic.DetailView):
    """Generic Detail view for posts."""

    model = Post
    template_name = 'blog/detail.html'
