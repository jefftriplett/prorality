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
    url(r'^(?P<organization_slug>[\w-]+)/(?P<pk>[0-9a-zA-Z]+)/$',
        views.ProposalDetail.as_view(),
        name='proposal_detail'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<pk>[0-9a-zA-Z]+)/delete/$',
        views.ProposalDelete.as_view(),
        name='proposal_delete'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<pk>[0-9a-zA-Z]+)/draft/$',
        views.ProposalDraft.as_view(),
        name='proposal_draft'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<pk>[0-9a-zA-Z]+)/raw/$',
        views.ProposalRawDetail.as_view(),
        name='proposal_raw_detail'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<pk>[0-9a-zA-Z]+)/update/$',
        views.ProposalUpdate.as_view(),
        name='proposal_update'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<pk>[0-9a-zA-Z]+)/vote/$',
        views.VoteFormView.as_view(),
        name='proposal_vote_form'),
    url(r'^(?P<organization_slug>[\w-]+)/(?P<pk>[0-9a-zA-Z]+)/withdrawn/$',
        views.ProposalWithdrawn.as_view(),
        name='proposal_withdrawn'),
]
