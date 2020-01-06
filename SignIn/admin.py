from django.contrib import admin
from .models import User, Sign, SignLog


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'token', '共关注', '已签到', '未签到', '是否有效用户', 'created_time')
    search_fields = ('id', 'username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user.username)


class SignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fid', 'is_sign', 'retry_time', 'status', 'user')
    search_fields = ('id', 'name', 'fid', 'status', 'user__username')


class SignLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_time', 'ret_log', 'user')
    search_fields = ('id', 'name', 'user__username')


admin.site.register(User, UserAdmin)
admin.site.register(Sign, SignAdmin)
admin.site.register(SignLog, SignLogAdmin)
