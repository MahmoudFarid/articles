import factory

from factory.django import DjangoModelFactory as Factory
from django.contrib.auth.models import Permission

from ..models import Blog
from articles.users.tests.factories import UserFactory


class Blogfactory(Factory):
    user = user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph', nb_sentences=5)
    content = factory.Faker('paragraph', nb_sentences=10)
    gdoc_link = 'https://docs.google.com/document/d/1NcF8_6ZMraTXp7H7DVzR6pbqzJgNIyg3gYLUUoFoYe8/edit'
    status = factory.Faker('random_element', elements=[sttaus[0] for sttaus in Blog.STATUS_CHOICES])

    class Meta:
        model = Blog


def create_user_writer_with_permission():
    user = UserFactory()
    write_blogs_perm = Permission.objects.filter(codename='can_write_blogs').first()
    user.user_permissions.add(write_blogs_perm)
    return user


def create_editor_user_with_permission():
    user = UserFactory()
    review_blogs_perm = Permission.objects.filter(codename='can_review_blogs').first()
    user.user_permissions.add(review_blogs_perm)
    return user
