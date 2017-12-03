from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from organizations.backends import invitation_backend, registration_backend


urlpatterns = [
    # our applications
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^proposals/', include('proposals.urls', namespace='proposals')),

    # third-party applications
    url(r'^accounts/', include('allauth.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^invitations/', include(invitation_backend().get_urls())),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^register/', include(registration_backend().get_urls())),

    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
