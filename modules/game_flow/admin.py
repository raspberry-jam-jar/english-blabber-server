from django.contrib import admin

import game_flow.models as m


@admin.register(m.UserHero)
class UserHeroAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'capacity', 'coins', )


@admin.register(m.UserGift)
class UserGiftAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'hero', 'quantity', )
