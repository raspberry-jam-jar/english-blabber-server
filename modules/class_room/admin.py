from django.contrib import admin, auth

import class_room.models as m
from .forms import UserForm


admin.site.unregister(auth.models.Group)
admin.site.unregister(auth.models.User)


class UserInline(admin.TabularInline):
    fields = (('first_name', 'last_name'), 'username', 'date_of_birth',
              'image', 'role', 'learning_group')

    model = m.User
    form = UserForm


@admin.register(m.LearningGroup)
class LearningGroupAdmin(admin.ModelAdmin):
    inlines = [UserInline, ]


@admin.register(m.User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('role', 'learning_group')

    fields = (('first_name', 'last_name'), 'username', 'email', 'date_of_birth',
              'image', 'role', 'learning_group')
    form = UserForm

    def save_model(self, request, obj, form, change):
        if obj.role in ('admin', 'teacher'):
            obj.is_superuser = True
            obj.is_staff = True

        super().save_model(request, obj, form, change)


@admin.register(m.SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'user',)
    readonly_fields = ('first_name', 'last_name',)

    def has_add_permission(self, request):
        return False
