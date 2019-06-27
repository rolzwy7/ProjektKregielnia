from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from kregielnia_app.models import Profil, Przekaski, Rezerwacja, PrzekaskiZamowienie, Przekaski, Rezerwacja
from kregielnia_app.models import Tor
from datetime import datetime
from datetime import timedelta
from django.views.generic.list import ListView
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


class HomepageView(View):
    def get(self, request):
        return render(request, "kregielnia_app/homepage.html", {})


@method_decorator(login_required(login_url='/logowanie/'), name="dispatch")
class ZamowienieSuccessView(View):
    def get(self, request):
        return render(request, "kregielnia_app/zamowienie-success.html", {})

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MapView(View):
    def get(self, request):
        return render(request, "kregielnia_app/mapa.html", {})


class GaleriaView(View):
    def get(self, request):
        return render(request, "kregielnia_app/galeria.html", {})


class CennikView(View):
    def get(self, request):
        data = {"przekaski": Przekaski.objects.all()}
        return render(request, "kregielnia_app/cennik.html", data)


class RezerwacjeView(View):
    def get(self, request):
        data = {
            "przekaski": Przekaski.objects.all(),
            "tory": Tor.objects.all(),
        }
        return render(request, "kregielnia_app/rezerwacje.html", data)

    def post(self, request):
        # Get params
        data_rozpoczecia = request.POST.get("data_rozpoczecia")
        godzina_rozpoczecia = request.POST.get("godzina_rozpoczecia")
        ilosc_torow = request.POST.get("ilosc_torow")
        ilosc_osob = request.POST.get("ilosc_osob")
        ilosc_godzin = request.POST.get("ilosc_godzin")
        dodatkowe_informacje = request.POST.get("dodatkowe_informacje")


        if int(ilosc_torow) * 6 < int(ilosc_osob):
            data = {
                "failed": "Na 1 torze może grać maksymalnie 6 osób. Za duża ilość osób w stosunku do liczby torów.",
                "przekaski": Przekaski.objects.all(),
                "tory": Tor.objects.all()
            }
            return render(request, "kregielnia_app/rezerwacje.html", data)

        if int(ilosc_godzin) == 0:
            data = {
                "failed": "Nie wybrano ilości godzin",
                "przekaski": Przekaski.objects.all(),
                "tory": Tor.objects.all()
            }
            return render(request, "kregielnia_app/rezerwacje.html", data)

        params = [
            data_rozpoczecia,
            godzina_rozpoczecia,
            ilosc_torow,
            ilosc_osob,
            ilosc_godzin
        ]
        if not all(params):
            return HttpResponseBadRequest(content=b"400 Bad Request")

        przekaski = []
        for k, v in request.POST.items():
            if k.startswith("przekaska_") and v != 0:
                k_t = k.replace("przekaska_", "")
                przekaski.append( (int(k_t), int(v)) )

        tory = []
        for k, v in request.POST.items():
            if k.startswith("tor_"):
                tory.append(k)

        if dodatkowe_informacje:
            dodatkowe_informacje = ""

        if tory:
            dodatkowe_informacje += "\n\nPreferowane tory:\n" + "\n".join(tory)
        else:
            dodatkowe_informacje = None

        year, month, day = data_rozpoczecia.split("-")
        hour, minute = godzina_rozpoczecia.split(":")
        second = 0
        year, month, day = int(year), int(month), int(day)
        hour, minute = int(hour), int(minute)

        dt_rozpoczecia = datetime(
            year=year, month=month,
            day=day, hour=hour,
            minute=minute, second=second
        )

        dt_zakonczenia = dt_rozpoczecia + timedelta(hours=int(ilosc_godzin))


        # # WARNING: AZNE
        test_ = Rezerwacja.objects.filter(
            (
                Q(dt_zakonczenia__gt=dt_rozpoczecia)
            &
                Q(dt_rozpoczecia__lt=dt_rozpoczecia)
            )
            |
            (
                Q(dt_zakonczenia__gt=dt_zakonczenia)
            &
                Q(dt_rozpoczecia__lt=dt_zakonczenia)
            )
        )
        # import pdb; pdb.set_trace()
        tory_kolidujace = 0
        for _ in test_:
            tory_kolidujace += int(_.ilosc_torow)
        # import pdb; pdb.set_trace()
        war = (12 - tory_kolidujace - int(ilosc_torow))
        if war < 0:
            data = {
                "failed": "Podana ilość torów jest niedostępna w tym czasie",
                "przekaski": Przekaski.objects.all(),
                "tory": Tor.objects.all()
            }
            return render(request, "kregielnia_app/rezerwacje.html", data)
        # import pdb; pdb.set_trace()

        rezerwacja = Rezerwacja(
            user_id=Profil.objects.get(user=request.user.id),
            dt_rozpoczecia=dt_rozpoczecia,
            dt_zakonczenia=dt_zakonczenia,
            ilosc_osob=int(ilosc_osob),
            ilosc_torow=int(ilosc_torow),
            ilosc_godzin=int(ilosc_godzin),
            dod_info=dodatkowe_informacje
        )
        rezerwacja.save()

        # Zapisz przekaski
        for p in przekaski:
            for i in range(p[1]):
                przekaski_zamowienie = PrzekaskiZamowienie(
                    rezerwacja_id=rezerwacja,
                    przekaski_id=Przekaski.objects.get(id=p[0])
                )
                przekaski_zamowienie.save()

        return redirect("zamowienie_success")


class LogowanieView(View):
    def get(self, request):
        data = {"next": request.GET.get("next")}
        return render(request, "kregielnia_app/logowanie.html", data)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        next = request.POST.get("next")
        if username is None or password is None:
            return HttpResponseBadRequest("Auth error")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next) if next else redirect("homepage")
        else:
            return render(request, "kregielnia_app/logowanie.html", {
                "auth_failed": "Email lub hasło są niepoprawne"
            })


class RejestracjaView(View):
    def get(self, request):
        return render(request, "kregielnia_app/rejestracja.html", {})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_r = request.POST.get("password_r")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        regulamin = request.POST.get("regulamin")
        newsletter = request.POST.get("newsletter")

        nr_telefonu = request.POST.get("nr_telefonu")

        regulamin = True if regulamin == "on" else False
        newsletter = True if newsletter == "on" else False

        if password != password_r:
            return render(request, "kregielnia_app/rejestracja.html", {
                "failed": "Hasła nie są takie same"
            })

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Zapisać regulamin i newsletter w profilu
        profil = Profil.objects.get(user=user)
        profil.regulamin = regulamin
        profil.newsletter = newsletter
        profil.nr_telefonu = nr_telefonu
        profil.save()
        return redirect("rejestracja_sukces")


class WylogowanieView(View):
    def get(self, request):
        logout(request)
        return render(request, "kregielnia_app/homepage.html", {})


class RegisterSuccessView(View):
    def get(self, request):
        return render(request, "kregielnia_app/register_success.html", {})


@method_decorator(login_required(login_url='/logowanie/'), name="dispatch")
class MojeRezerwacjeListView(ListView):
    model = Rezerwacja
    paginate_by = 1000
    ordering = ['-date_added']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        prof = Profil.objects.get(user=self.request.user.id)
        context = self.model.objects.filter(
            user_id=prof
        )
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ZamowienieDetailView(generic.DetailView):
    model = Rezerwacja

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["has_access"] = self.object.user_id.user_id == self.request.user.id

        context["przekaski"] = PrzekaskiZamowienie.objects.filter(rezerwacja_id=self.object)

        context["buty_cena"] = self.object.ilosc_osob * 5

        przekaski_cena = 0
        for _ in context["przekaski"]:
            przekaski_cena += _.przekaski_id.cena
        context["przekaski_cena"] = przekaski_cena
        context["po_17"] = self.object.dt_rozpoczecia.hour > 17

        if self.object.dt_rozpoczecia.weekday() in [0, 1, 2, 4]:
            if context["po_17"]:
                context["za_tor"] = 69
                context["za_tor_suma"] = 69 * self.object.ilosc_torow * self.object.ilosc_godzin
            else:
                context["za_tor"] = 49
                context["za_tor_suma"] = 49 * self.object.ilosc_torow * self.object.ilosc_godzin
        if self.object.dt_rozpoczecia.weekday() in [5]:
            if context["po_17"]:
                context["za_tor"] = 89
                context["za_tor_suma"] = 89 * self.object.ilosc_torow * self.object.ilosc_godzin
            else:
                context["za_tor"] = 49
                context["za_tor_suma"] = 49 * self.object.ilosc_torow * self.object.ilosc_godzin
        if self.object.dt_rozpoczecia.weekday() in [6, 7]:
            if context["po_17"]:
                context["za_tor"] = 89
                context["za_tor_suma"] = 89 * self.object.ilosc_torow * self.object.ilosc_godzin
            else:
                context["za_tor"] = 79
                context["za_tor_suma"] = 79 * self.object.ilosc_torow * self.object.ilosc_godzin

        context["suma_final"] = context["za_tor_suma"] + context["buty_cena"] + context["przekaski_cena"]

        return context
