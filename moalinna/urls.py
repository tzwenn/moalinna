from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='authorized_keys', permanent=False)),
    path('admin/', admin.site.urls),
    path('authorized_keys/', include('authorized_keys.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]

if settings.OIDC_ENABLED:
	urlpatterns += [
		path('oidc/', include('mozilla_django_oidc.urls')),
	]