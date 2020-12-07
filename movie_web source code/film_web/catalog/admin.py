from django.contrib import admin
from catalog.models import Users, Movies, Ratings

# Register your models here.
admin.site.register(Users)
admin.site.register(Movies)
admin.site.register(Ratings)
