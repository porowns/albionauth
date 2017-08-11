# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import AlbionCharacter, Craft, PlayerCraft

@admin.register(AlbionCharacter)
class AlbionCharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'get_username')

    def get_username(self, albioncharacter):
        return albioncharacter.user.username

@admin.register(Craft)
class AlbionCraftAdmin(admin.ModelAdmin):
    list_display = ('item', 'building')

@admin.register(PlayerCraft)
class AlbionPlayerCraftAdmin(admin.ModelAdmin):
    list_display = ('craftname', 'tier', 'get_username')

    def craftname(self, playercraft):
        return playercraft.craft.item
    def get_username(self, playercraft):
        return playercraft.character.name

