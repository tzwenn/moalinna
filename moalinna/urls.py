from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='authorized_keys', permanent=False)),
    path('admin/', admin.site.urls),
    path('authorized_keys/', include('authorized_keys.urls')),
]
