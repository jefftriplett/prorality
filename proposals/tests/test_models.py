from test_plus.test import TestCase

from ..factories import ProposalFactory
from whatnots import factories as org_factories


class ProposalModel(TestCase):

    def test_creation(self):
        organization = org_factories.OrganizationFactory()
        proposal = ProposalFactory(
            organization=organization,
        )
        self.assertEqual(proposal.pk, 1)
