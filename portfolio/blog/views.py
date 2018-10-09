"""All Views."""
from django.conf import settings
from django.views import generic
from .models.post import Post


class IndexView(generic.ListView):
    """Landspage view.

    Shows latest six published posts. Post is published when pub_date is lower
    to today
    """

    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the last six published posts."""
        el_per_page = settings.CONSTS.getint(
            'portfolio.blog',
            'el_per_page'
        )

        posts = []

        if ('tag' in self.request.GET.keys()):

            def tags_name_in_all(objects, filters):
                """Return all posts with all tags into list.

                Recursive method for extract all posts with
                all tags into filters field.
                """
                if not filters:
                    return objects
                return tags_name_in_all(objects.filter(
                    tags__name=filters.pop()), filters
                )

            posts = tags_name_in_all(
                Post.objects,
                # TODO[index.html -> request.GET.urlencode] Can generate a...
                # ... url with duplicates, then it's required a set conversion
                # list(self.request.GET.getlist('tag')[:])
                list(tuple(set(self.request.GET.getlist('tag')))[:])
            )

        else:
            posts = Post.objects

        return posts.order_by('-pub_date')[:el_per_page]


class DetailView(generic.DetailView):
    """Generic Detail view for posts."""

    model = Post
    template_name = 'blog/detail.html'
