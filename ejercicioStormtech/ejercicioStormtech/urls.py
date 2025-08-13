from core.views import *
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('paquetes/listar/', PaqueteListar.as_view(), name='paquetes-lista'),
    path('paquetes/crear/', PaqueteCrear.as_view(), name='paquetes-crear'),
    path('planillas/asignar-paquetes/', AsignarPaquetes.as_view(), name='asignar-paquetes'),
    path('planillas/<int:pk>/resumen/', PlanillaResumenView.as_view(), name='planilla-resumen'),
    path('planillas/<int:planilla_id>/pasar-a-distribucion/',PlanillaADistribucion.as_view(),name='pasar-a-distribucion'),
    path('planillas/item/actualizar-fallo/',ModificarMotivoFallo.as_view(),name='actualizar-fallo-otem'),
    ]
