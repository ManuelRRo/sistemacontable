
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('contabilidad.urls')),
    path('usuario/', include('django.contrib.auth.urls')),
    path('usuario/',include('usuarios.urls')),
]
