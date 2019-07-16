from django.conf.urls import url
from django.conf import settings

from .models import Redirect


def group_arguments(seq, group=254):
    """
        group the list into lists of 254 items each.

        This is due to argument restrictions in python.
        http://docs.djangoproject.com/en/dev/topics/http/urls/#patterns
    """
    return (seq[pos:pos + group] for pos in list(range(0, len(seq), group)))


def get_redirect_patterns():
    """
        Gets the redirect patterns out of the database
        and assigns them to the django patterns object.
    """
    site_id = settings.SITE_ID
    url_patterns = []
    url_list = []
    db_filters = {
        'status': 1,
        'site': site_id
    }

    redirects = Redirect.objects.filter(**db_filters)
    for r in redirects:
        extra = {}
        pattern = r'^%s$' % r.from_url

        extra.update({'url': '%s' % r.to_url})

        if r.http_status == 302:
            extra.update({'permanent': False})
            url_list.append(url(pattern, 'redirect_to', extra))
        else:
            url_list.append(url(pattern, 'redirect_to', extra))

    arg_groups = list(group_arguments(url_list))
    for args in arg_groups:
        url_patterns += url('redirect.views', *args)

    return url_patterns
