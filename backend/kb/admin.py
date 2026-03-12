from django.contrib import admin
from .models import KBChunk, KBDocument, FAQ
# Register your models here.
admin.site.register(FAQ)
admin.site.register(KBDocument)
admin.site.register(KBChunk)