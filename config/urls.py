from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from organizations.backends import invitation_backend, registration_backend


urlpatterns = [
    url(r'^proposals/', include('proposals.urls', namespace='proposals')),

    url(r'^invitations/', include(invitation_backend().get_urls())),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^register/', include(registration_backend().get_urls())),

    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
