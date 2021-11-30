from django.contrib import admin

from main.models import *

class PostImageInLine(admin.TabularInline):
    model = Image
    max_num = 9
    min_num = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInLine, ]
    list_display = ('tag', )


admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Rating)
