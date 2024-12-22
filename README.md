# django-aioredis
This package provides a custom cache backend for Django that integrates with the asynchronous capabilities of the aioredis library. It allows seamless caching operations in Django applications while supporting asynchronous workflows for improved performance and scalability.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install django-aioredis
```

## Settings

You will need to add below modifications to project's settings.py

```python

# you can set this backend as default cache backend
CACHES = {
    'default': {
        'BACKEND': 'myapp.cache.AsyncRedisCache',
        'LOCATION': 'redis://localhost:6379/0',
    }
}

# or you can set this along default cache backend
REDIS_URL = 'redis://localhost:6379'
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    },
    "async-cache": {
        'BACKEND': 'myapp.cache.AsyncRedisCache',
        'LOCATION': REDIS_URL,
    }
}
```

## Usage

```python
from channels.db import database_sync_to_async

# If you have set it as default backend, try this code:
from django.core.cache import cache

async def get_profile(pid: int) -> Profile | None:
    key = f"profile-{pid}"
    if key in cache:
        return cache.aget(key)
    profile = database_sync_to_async(Profile.objects.get(pk=pid))
    if profile:
        cache.aset(key, profile, timeout=60)

# for sync functions you can easily use this:
def get_profile(pid: int) -> Profile | None:
    key = f"profile-{pid}"
    if key in cache:
        return cache.get(key)
    profile = Profile.objects.get(pk=pid)
    if profile:
        cache.set(key, profile, timeout=60)

# If you have used it along default cache then:
from django.core.cache import caches
cache = caches["default"]
async_cache = caches["async-cache"]

# The only modification needed is in object name so in case of async functions you can use async_cache.aget or async_cache.aset and for reqular functions simply obey the oldschool approach

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
