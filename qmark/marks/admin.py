from django.contrib import admin
from .models import Post, Thing, Room, Comment, Company


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ['h1']}

class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ['number']}
        
class ThingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ['number']}

class CommentAdmin(admin.ModelAdmin):
    pass

class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Thing, ThingAdmin)
admin.site.register(Comment, CommentAdmin)
# Register your models here.
