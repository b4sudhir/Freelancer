from django.contrib import admin
from .models import auth,profile,skills
# Register your models here.
admin.site.register(auth)
admin.site.register(profile)
admin.site.register(skills)
