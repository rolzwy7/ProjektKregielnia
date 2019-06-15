from django.contrib import admin
from kregielnia_app import models


@admin.register(models.Tor)
class TorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Przekaski)
class PrzekaskiAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Buty)
class ButyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Rezerwacja)
class RezerwacjaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PrzekaskiZamowienie)
class PrzekaskiZamowienieAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ButyZamowienie)
class ButyZamowienieAdmin(admin.ModelAdmin):
    pass
