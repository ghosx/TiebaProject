from django.contrib import admin
from .models import Tieba,User

class TiebaAdmin(admin.ModelAdmin):
    list_display = ('name','fid','add_time',)
    search_fields = ('name','fid',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','bduss','created_time',)
    search_fields = ('username',)

admin.site.register(Tieba, TiebaAdmin)
admin.site.register(User, UserAdmin)