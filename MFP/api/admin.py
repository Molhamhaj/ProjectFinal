from django.contrib.auth.models import Group
from django.contrib import admin
from . import models
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    exclude = ('first_name', 'last_name', 'groups', 'user_permissions',
               'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    list_display = ('pk', 'username', 'email', 'is_admin', 'user_role')
    list_filter = ('is_staff', 'user_role',)

    def is_admin(self, obj):
        pl = "✔️" if obj.is_staff else "❌"
        return pl
    
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Country)
admin.site.register(models.UserRoles)
admin.site.register(models.Customer)
admin.site.register(models.AirlineCompany)
admin.site.register(models.Administrator)
admin.site.register(models.Flight)
admin.site.register(models.Ticket)


admin.site.site_header = "🎮 Flight Management System ✨"
admin.site.site_title = "Admin"
admin.site.index_title = "Website Administration"

admin.site.unregister(Group)
