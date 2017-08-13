# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AlbionCharacter(models.Model):
    role_choices = (
            ("Tank", "Tank"),
            ("Ranged DPS", "Ranged DPS"),
            ("Melee DPS", "Melee DPS"),
            ("Healer", "Healer")
            )
    name = models.CharField(max_length=32)
    discord = models.CharField(max_length=32)
    role = models.CharField(max_length=32, choices=role_choices)
    secondary = models.CharField(max_length=32, choices=role_choices, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Craft(models.Model):
    building_choices = (
            ("Toolmaker", "Toolmaker"),
            ("Warrior", "Warrior"),
            ("Mage", "Mage"),
            ("Hunter", "Hunter"),
            ("Alchemist", "Alchemist"),
            ("Cook", "Cook"),
            ("Saddler", "Saddler")
            )
    item = models.CharField(max_length=32)
    building = models.CharField(max_length=32, choices=building_choices)

    def __str__(self):
        return self.item

class PlayerCraft(models.Model):
    craft = models.ForeignKey("Craft", on_delete=models.CASCADE)
    character = models.ForeignKey("AlbionCharacter", on_delete=models.CASCADE)
    tier = models.IntegerField(default=0)

    def __str__(self):
        return self.craft.item

class Static(models.Model):
    """
    Confusing name, I know. A Static is equivilent to a group that doesn't change in Albion Online, and is just a
    terminology.
    """
    name = models.CharField(max_length=32)
    leader = models.ForeignKey("AlbionCharacter", on_delete=models.CASCADE, related_name="leader")
    members = models.ManyToManyField("AlbionCharacter", blank=True, null=True)
    description = models.CharField(max_length=500)
