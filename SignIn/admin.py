from django.contrib import admin
from .models import User, Sign, SignLog


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'token', 'all_bind', 'signed', 'unsigned', 'created_time')
    search_fields = ('username',)


class SignAdmin(admin.ModelAdmin):
    list_display = ('name', 'fid', 'is_sign', 'status', 'retry_times', 'user')
    search_fields = ('name', 'fid', 'status', 'user')


class SignLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time', 'ret_log', 'user')
    search_fields = ('name', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Sign, SignAdmin)
admin.site.register(SignLog, SignLogAdmin)
