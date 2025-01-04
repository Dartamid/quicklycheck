from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Account

User = get_user_model()


class AccountAdmin(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'


@admin.register(User)
class CustomizedUserAdmin(UserAdmin):
    model = User
    list_display = ('account_name',)
    inlines = [AccountAdmin]
    
    def account_name(self, obj):
        return f'{obj.account.last_name} {obj.account.first_name} {obj.account.patronymic}'
        

