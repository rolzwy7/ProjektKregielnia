from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save

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


class Profil(models.Model):
    class Meta:
        verbose_name_plural = "Profile"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    regulamin = models.BooleanField(default=False, null=True)
    newsletter = models.BooleanField(default=False, null=True)
    nr_telefonu = models.CharField(max_length=9, null=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profil.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except Exception as e:
            pass


class Tor(models.Model):
    class Meta:
        verbose_name_plural = "Tory"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    nr_toru = models.CharField(unique=True, null=False,
                               blank=False, max_length=3)

    def __str__(self):
        return "Tor %s" % self.nr_toru


class Przekaski(models.Model):
    class Meta:
        verbose_name_plural = "Przekąski"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    wycofana = models.BooleanField(default=False)

    nazwa = models.CharField(max_length=64, null=False, blank=False)
    cena = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.nazwa


class Buty(models.Model):
    class Meta:
        verbose_name_plural = "Buty"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64,
                            null=True, default="Buty do kręgli")
    stan = models.CharField(choices=STANY_BUTOW, max_length=1)
    rozmiar = models.CharField(choices=ROZMIARY_BUTOW, max_length=2)

    def __str__(self):
        return "%s (%s) [%s]" % (self.name, self.rozmiar, self.stan)


class Rezerwacja(models.Model):
    class Meta:
        verbose_name_plural = "Rezerwacje"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    user_id = models.ForeignKey("Profil", on_delete=models.CASCADE)
    dt_rozpoczecia = models.DateTimeField(null=False, blank=False)
    dt_zakonczenia = models.DateTimeField(null=False, blank=False)
    ilosc_osob = models.IntegerField(null=False, blank=False)
    ilosc_torow = models.IntegerField(null=False, blank=False)
    ilosc_godzin = models.IntegerField(null=False, blank=False)
    dod_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Rezerwacja %s" % self.dt_rozpoczecia


class PrzekaskiZamowienie(models.Model):
    class Meta:
        verbose_name_plural = "Przekąski Zamówienia"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    przekaski_id = models.ForeignKey("Przekaski", on_delete=models.CASCADE)
    rezerwacja_id = models.ForeignKey("Rezerwacja", on_delete=models.CASCADE)

    def __str__(self):
        return "Przekąska %s - zamówienie: %s" % (self.przekaski_id, self.rezerwacja_id)


class ButyZamowienie(models.Model):
    class Meta:
        verbose_name_plural = "Buty Zamówienia"

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    buty_id = models.ForeignKey("Buty", on_delete=models.CASCADE)
    rezerwacja_id = models.ForeignKey("Rezerwacja", on_delete=models.CASCADE)
