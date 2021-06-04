from django.contrib import admin, auth
from django.conf.urls import url
from django.urls import path, include
from . import views
from pis import views as core_views

urlpatterns = [
    # path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    url(r'', include('pis.urls')),
    url(r'', include('users.urls')),
    # url(r'^accounts/', include('django_registration.backends.one_step.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/forgot-password/', views.forgotPassword),
    # url(r'^logout/$', auth.logout, name="locked"),
    url(r'^logout/$', auth.logout, {"next_page": '/'}),
    # url(r'^locked/$', views.locked, name='lock'),
]

handler404 = core_views.handler404