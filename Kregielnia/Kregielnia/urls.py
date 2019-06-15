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
    path('', views.HomepageView.as_view(), name="homepage"),
]

# Add media for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
