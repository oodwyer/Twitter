from django.contrib import admin
from core.models import Tweet
from core.models import Hashtag

# Register your models here.

admin.site.register(Tweet)
admin.site.register(Hashtag)