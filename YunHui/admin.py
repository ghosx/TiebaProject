from django.contrib import admin
from .models import Tieba,User,Sign

class TiebaAdmin(admin.ModelAdmin):
    list_display = ('name','fid','time','success','fail','add_time',)
    search_fields = ('name','fid',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','token','created_time','绑定贴吧','已签到','未签到','云回贴吧')
    search_fields = ('username',)

class SignAdmin(admin.ModelAdmin):
    list_display = ('name','fid','level_id','cur_score','is_sign',)
    search_fields = ('name','fid','level_id',)

admin.site.register(Tieba, TiebaAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Sign, SignAdmin)