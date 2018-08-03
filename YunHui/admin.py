from django.contrib import admin
from .models import TiebaYunHui,TiebaUser

class TiebaAdmin(admin.ModelAdmin):
    list_display = ('name','fid','add_time',)
    search_fields = ('name','fid',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','bduss','created_time',)
    search_fields = ('username',)

admin.site.register(TiebaYunHui,TiebaAdmin)
admin.site.register(TiebaUser,UserAdmin)