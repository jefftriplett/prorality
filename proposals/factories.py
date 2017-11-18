import factory


class ProposalFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'proposals.Proposal'
