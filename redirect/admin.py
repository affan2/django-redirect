from django.contrib import admin
import importlib

from .models import Redirect
from . import dynamic_urls


class RedirectAdmin(admin.ModelAdmin):
    list_display = ['from_url', 'to_url', 'site', 'http_status', 'uses_regex', 'status']

    def save_model(self, request, object_to_be_saved, form, change):
        instance = form.save()
        # for sites that are not in debug mode reload
        # the dynamic urls, i'm not sure if this is the
        # best way though
        importlib.reload(dynamic_urls)
        return instance


admin.site.register(Redirect, RedirectAdmin)
