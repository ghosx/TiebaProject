from django.contrib import admin
from .models import User, Sign, SignLog, SignTotal


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'email_notice', 'token',
                    '共关注', '已签到', '未签到', '是否有效用户', 'created_time', 'update_time')
    list_editable = ('email', 'email_notice')
    search_fields = ('username', 'email')
    list_display_links = ('username',)
    list_per_page = 30
    date_hierarchy = 'created_time'
    actions = ('make_new_user',)

    def make_new_user(self, request, queryset):  # 定义动作
        rows_updated = queryset.update(flag=0)
        if rows_updated == 1:
            message_bit = "one user changed"
        else:
            message_bit = "%s users changed" % rows_updated
        self.message_user(request, "%s successfully ." % message_bit)

    make_new_user.short_description = "刷新关注的贴吧并签到"  # 重写动作显示名称

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user.username)


class SignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fid', 'is_sign',
                    'retry_time', 'status', 'user')
    search_fields = ('id', 'name', 'fid', 'status', 'user__username')
    actions = ['re_sign', ]

    def re_sign(self, request, queryset):  # 定义动作
        rows_updated = queryset.update(is_sign=0, retry_time=0, status="")
        if rows_updated == 1:
            message_bit = "one tieba resign"
        else:
            message_bit = "%s  tieba resign" % rows_updated
        self.message_user(request, "%s successfully ." % message_bit)

    re_sign.short_description = "重新签到"  # 重写动作显示名称

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        u = User.objects.get(username=request.user.username)
        return qs.filter(user=u)


class SignLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'update_time', 'ret_log', 'user')
    search_fields = ('id', 'name', 'user__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        u = User.objects.get(username=request.user.username)
        return qs.filter(user=u)


class SignTotalAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')


admin.site.register(User, UserAdmin)
admin.site.register(Sign, SignAdmin)
admin.site.register(SignLog, SignLogAdmin)
admin.site.register(SignTotal, SignTotalAdmin)
