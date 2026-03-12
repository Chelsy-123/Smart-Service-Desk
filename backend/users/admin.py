from django.contrib import admin
from .models import User, Agent, Admin, UserNotificationPreference
# Register your models here.
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Admin)
admin.site.register(UserNotificationPreference)