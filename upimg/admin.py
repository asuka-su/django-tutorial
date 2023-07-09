from django.contrib import admin

from .models import UserProfile, Photo

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    fields = ["username"]

class PhotoAdmin(admin.ModelAdmin):
    fields = ["uploader", "title", "image"]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Photo, PhotoAdmin)