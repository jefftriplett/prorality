import factory


class OrganizationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'organizations.Organization'


class OrganizationOwnerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'organizations.OrganizationOwner'


class OrganizationUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'organizations.OrganizationUser'
