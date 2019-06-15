from django.db import models

ROZMIARY_BUTOW = (
    ('32', 'Rozmiar 32'),
    ('33', 'Rozmiar 33'),
    ('34', 'Rozmiar 34'),
    ('35', 'Rozmiar 35'),
    ('36', 'Rozmiar 36'),
    ('37', 'Rozmiar 37'),
    ('38', 'Rozmiar 38'),
    ('39', 'Rozmiar 39'),
    ('40', 'Rozmiar 40'),
    ('41', 'Rozmiar 41'),
    ('42', 'Rozmiar 42'),
    ('43', 'Rozmiar 43'),
    ('44', 'Rozmiar 44'),
    ('45', 'Rozmiar 45'),
    ('46', 'Rozmiar 46'),
    ('47', 'Rozmiar 47'),
    ('48', 'Rozmiar 48'),
    ('49', 'Rozmiar 49')
)

STANY_BUTOW = (
    ('3', 'Nowe'),
    ('2', 'Lekko zużyte'),
    ('1', 'Mocno zużyte'),
    ('0', 'Do wymiany'),
)


class Tor(models.Model):
    class Meta:
        verbose_name_plural = "Tory"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    godzina_rozpoczecia = models.DateTimeField(null=False, blank=False)
    godzina_zakonczenia = models.DateTimeField(null=False, blank=False)
    nazwisko = models.CharField(null=False, blank=False, max_length=64)
    nr_toru = models.CharField(unique=True, null=False,
                               blank=False, max_length=3)


class Przekaski(models.Model):
    class Meta:
        verbose_name_plural = "Przekąski"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    wycofana = models.BooleanField(default=False)

    nazwa = models.CharField(max_length=64, null=False, blank=False)
    cena = models.IntegerField(null=False, blank=False)


class Buty(models.Model):
    class Meta:
        verbose_name_plural = "Buty"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64,
                            null=True, default="Buty do kręgli")
    stan = models.CharField(choices=STANY_BUTOW, max_length=1)
    rozmiar = models.CharField(choices=ROZMIARY_BUTOW, max_length=2)


class Rezerwacja(models.Model):
    class Meta:
        verbose_name_plural = "Rezerwacje"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    tor_id = models.ForeignKey("Tor", on_delete=models.PROTECT)
    nazwisko = models.CharField(null=False, blank=False, max_length=64)
    ilosc_osob = models.IntegerField(null=False, blank=False)


class PrzekaskiZamowienie(models.Model):
    class Meta:
        verbose_name_plural = "Przekąski Zamówienia"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    przekaski_id = models.ForeignKey("Przekaski", on_delete=models.PROTECT)
    rezerwacja_id = models.ForeignKey("Rezerwacja", on_delete=models.PROTECT)


class ButyZamowienie(models.Model):
    class Meta:
        verbose_name_plural = "Buty Zamówienia"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    buty_id = models.ForeignKey("Buty", on_delete=models.PROTECT)
    rezerwacja_id = models.ForeignKey("Rezerwacja", on_delete=models.PROTECT)
