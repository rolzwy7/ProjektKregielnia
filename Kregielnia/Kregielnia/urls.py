from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from kregielnia_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('mapa/', views.MapView.as_view(), name="mapa"),
    path('galeria/', views.GaleriaView.as_view(), name="galeria"),
    path('cennik/', views.CennikView.as_view(), name="cennik"),
    path('rezerwacje/', views.RezerwacjeView.as_view(), name="rezerwacje"),
    path('mapa/', views.MapView.as_view(), name="mapa"),
    path('logowanie/', views.LogowanieView.as_view(), name="logowanie"),
    path('rejestracja/', views.RejestracjaView.as_view(), name="rejestracja"),
    path('rejestracja_sukces/', views.RegisterSuccessView.as_view(), name="rejestracja_sukces"),
    path('wyloguj/', views.WylogowanieView.as_view(), name="logout"),
    path('moje_rezerwacje/', views.MojeRezerwacjeListView.as_view(), name="moje_rezerwacje"),
    path('zamownienie-success/', views.ZamowienieSuccessView.as_view(), name="zamowienie_success"),
    path('zamowienie/<int:pk>', views.ZamowienieDetailView.as_view(), name="zamowienie_detail"),
    path('', views.HomepageView.as_view(), name="homepage"),
]

# Add media for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
