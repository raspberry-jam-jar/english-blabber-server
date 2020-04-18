from django.contrib import admin

import game_skeleton.models as m


admin.site.register(m.Gift)
admin.site.register(m.HeroClass)


class GradationInline(admin.TabularInline):
    model = m.Gradation


@admin.register(m.Rule)
class RuleAdmin(admin.ModelAdmin):
    inlines = [GradationInline, ]


admin.site.register(m.Skill)
admin.site.register(m.Cristal)
admin.site.register(m.Penalty)
