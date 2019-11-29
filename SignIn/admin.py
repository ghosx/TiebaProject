from django.contrib import admin
from .models import User, Sign

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'token', 'created_time', 'all_bind', 'signed', 'unsigned')
#     search_fields = ('username',)
#
# class SignAdmin(admin.ModelAdmin):
#     list_display = ('name', 'fid', 'is_sign',)
#     search_fields = ('name', 'fid',)
#
# admin.site.register(User, UserAdmin)
# admin.site.register(Sign, SignAdmin)
