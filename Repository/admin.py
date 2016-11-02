from django.contrib import admin

from . import models

admin.site.register(models.Weibo)
admin.site.register(models.Topic)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Tags)
admin.site.register(models.UserProfile)
