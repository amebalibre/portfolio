"""All Views."""
from django.views import generic

from .models.post import Post


class IndexView(generic.ListView):
    """Landspage view.

    Shows latest six published posts. Post is published when pub_date is lower
    to today
    """

    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last six published posts."""
        return Post.objects.order_by('-pub_date')[:6]


class DetailView(generic.DetailView):
    """Generic Detail view for posts."""

    model = Post
    template_name = 'blog/detail.html'
