"""
URL configuration for locallibrery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

"""
    La clase RedirectView en Django es una vista genérica que te permite redirigir a los usuarios de una URL a otra de manera sencilla. En lugar de tener que escribir manualmente una vista que haga la redirección, puedes usar RedirectView para hacerlo con solo un par de configuraciones.
"""
urlpatterns = [
    path("admin/", admin.site.urls), 
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog', permanent=True)),
   
] 
#Add Django path site authentication urls (for login, logout, password managment )
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.STATIC_URL, domcument_root = settings.STATIC_ROOT)

