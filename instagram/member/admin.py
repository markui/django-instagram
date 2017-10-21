from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User


# class UserCreationForm(UserCreationForm):
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = UserCreationForm.Meta.fields + ('img_profile',)



class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('img_profile',)}),
    )
    # add_form = UserCreationForm
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('additional fields', {'fields': ('img_profile',)}),
    )


admin.site.register(User, UserAdmin)


