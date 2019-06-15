from django.shortcuts import render
from django.views.generic import View


class HomepageView(View):
    def get(self, request):
        return render(request, "kregielnia_app/homepage.html", {})


class MapView(View):
    def get(self, request):
        return render(request, "kregielnia_app/mapa.html", {})


class GaleriaView(View):
    def get(self, request):
        return render(request, "kregielnia_app/galeria.html", {})


class CennikView(View):
    def get(self, request):
        return render(request, "kregielnia_app/cennik.html", {})


class RezerwacjeView(View):
    def get(self, request):
        return render(request, "kregielnia_app/rezerwacje.html", {})


class LogowanieView(View):
    def get(self, request):
        return render(request, "kregielnia_app/logowanie.html", {})


class RejestracjaView(View):
    def get(self, request):
        return render(request, "kregielnia_app/rejestracja.html", {})
