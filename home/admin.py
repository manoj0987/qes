from django.contrib import admin
from .models import *

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title','user','add_time')
    search_fields = ('title','detail')
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Upvote)
admin.site.register(Downvote)