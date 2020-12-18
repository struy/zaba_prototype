import redis
from django.conf import settings


def fav_count(request):
    """Return len of favorites ads"""
    r = redis.Redis(connection_pool=settings.POOL)
    count = 0
    if request.user.id:
        count = r.get(f'Author:fav:{request.user.id}')
        if count:
            count = count.decode('utf-8')
    if not count:
        count = 0
    return {'fav_count': count}
