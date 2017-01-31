from django.contrib import admin
from virtual_league.models import *

# Register your models here.

class PlayerScoreAdmin(admin.TabularInline):
    model = PlayerScore

class PlayerAdmin(admin.ModelAdmin):
    inlines = (PlayerScoreAdmin, )
    list_display = ('name', 'position')
    list_filter = ['position']
    radio_fields = {"position": admin.HORIZONTAL}
    search_fields = ('name', 'position')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Game)
admin.site.register(UserProfile)
