from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<organization_slug>[\w-]+)/$',
        views.ProposalList.as_view(),
        name='proposal_list'),
    url(r'^(?P<organization_slug>[\w-]+)/by/(?P<status>[\w-]+)/$',
        views.ProposalList.as_view(),
        name='proposal_list_by_status'),
    url(r'^(?P<organization_slug>[\w-]+)/create/$',
        views.ProposalCreate.as_view(),
        name='proposal_create'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<hashid>[\w-]+)/$',
        views.ProposalDetail.as_view(),
        name='proposal_detail'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<hashid>[\w-]+)/delete/$',
        views.ProposalDelete.as_view(),
        name='proposal_delete'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<hashid>[\w-]+)/update/$',
        views.ProposalUpdate.as_view(),
        name='proposal_update'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<hashid>[\w-]+)/vote/$',
        views.VoteFormView.as_view(),
        name='proposal_vote_form'),
]
