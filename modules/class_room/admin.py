from django.contrib import admin, auth

import class_room.models as m
from .forms import UserForm


admin.site.unregister(auth.models.Group)


class UserInline(admin.TabularInline):
    model = m.LearningGroup.users.through
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(m.LearningGroup)
class LearningGroupAdmin(admin.ModelAdmin):
    inlines = [UserInline, ]

    fields = ('description', )


@admin.register(m.User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('role', )

    fields = (('first_name', 'last_name'), 'username', 'email',
              'date_of_birth', 'image', 'role', )
    inlines = [UserInline, ]
    form = UserForm

    def save_model(self, request, obj, form, change):
        if obj.role in ('admin', 'teacher'):
            obj.is_superuser = True
            obj.is_staff = True

        super().save_model(request, obj, form, change)


@admin.register(m.SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'datetime_created',
                    'platform')
    list_editable = ('user', )
    list_filter = ('datetime_created', )
    fields = ('first_name', 'last_name', 'user',)
    readonly_fields = ('first_name', 'last_name',)

    def has_add_permission(self, request):
        return False
