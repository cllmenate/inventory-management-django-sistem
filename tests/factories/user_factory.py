"""User factory for testing."""

import factory
from django.contrib.auth.models import User, Permission


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password after creation."""
        if not create:
            return
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("testpass123")

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        """Add permissions after creation."""
        if not create:
            return
        if extracted:
            self.user_permissions.set(extracted)

    @factory.post_generation
    def all_permissions(self, create, extracted, **kwargs):
        """Add all permissions if requested."""
        if not create:
            return
        if extracted:
            permissions = Permission.objects.all()
            self.user_permissions.set(permissions)
