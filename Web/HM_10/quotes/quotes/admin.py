from django.contrib import admin
from .models import Author, Quote, Tag

admin.site.register(Author)
admin.site.register(Quote)
admin.site.register(Tag)
