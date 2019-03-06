from django.core.cache import cache
from django.http import HttpResponse


def cache_wrapper(job):

    def cache_wrap(*args, **kwargs):
        request = args[0]
        name = 'analytics/profile/'+str(request.user.id)
        data = cache.get(name)
        if data:
            if type(data) is dict and data.get('content'):
                return HttpResponse(
                    data.get('content'),
                    content_type=data.get('content_type'),
                    status=200
                )
            return data
        data = job(*args, **kwargs)
        if hasattr(data, 'rendered_content'):
            content = data.rendered_content
            view_data = {
                "content_type": data['Content-Type'],
                "content": content
            }
            cache.set(name, view_data, None)
        else:
            cache.set(name, data, None)
        return data

    return cache_wrap
