from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<organization_slug>[\w-]+)/$', views.ProposalList.as_view(), name='proposal_list'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<hashid>[\w-]+)/$', views.ProposalDetail.as_view(), name='proposal_detail'),
    # url(r'^(?P<hashid>.*)/$', views.ProposalDetail.as_view(), name='proposal_detail'),
]
