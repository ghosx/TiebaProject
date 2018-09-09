from django.contrib import admin
from .models import Tieba,User,Sign,Robot

class TiebaAdmin(admin.ModelAdmin):
    list_display = ('name','fid','time','success','fail','add_time',)
    search_fields = ('name','fid',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','token','created_time','绑定贴吧','已签到','未签到','云回贴吧')
    search_fields = ('username',)

class SignAdmin(admin.ModelAdmin):
    list_display = ('name','fid','level_id','cur_score','is_sign',)
    search_fields = ('name','fid','level_id',)

class RobotAdmin(admin.ModelAdmin):
    list_display = ('thread_id','title','username','is_fans','fname','content','time')
    search_fields = ('thread_id','title','username','fname','content','time')

admin.site.register(Tieba, TiebaAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Sign, SignAdmin)
admin.site.register(Robot,RobotAdmin)