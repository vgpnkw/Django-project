import pytest
from django.contrib.auth.models import User, Group, Permission

from products.models import Product, Category


@pytest.fixture
def user_admin(db) -> User:
    group = Group.objects.create(name="app_user")
    change_user_permissions = Permission.objects.filter(
        codenamein=["change_user", "view_user"],
    )
    group.permissions.add(change_user_permissions)
    user = User.objects.create_user("First")
    user.groups.add(group)
    return user


@pytest.fixture
def user_test(db) -> User:
    group = Group.objects.create(name="app_user")
    change_user_permissions = Permission.objects.filter(
        codenamein=["change_user", "view_user"],
    )
    group.permissions.add(change_user_permissions)
    user = User.objects.create_user("Second")
    user.groups.add(group)
    return user


def test_should_create_two_users(user_admin: User, user_test: User) -> None:
    assert user_admin.pk != user_test.pk


@pytest.mark.parametrize("category", ['handy', 'tablet'])
def test_weapon_type(db, category):
    types = Category.objects.create()
    types.name = category
    types.save()
    assert types.str() == category


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username='vitalik', email='vitalik@yandex.ru', password='2281337')
    user.save()
    return user
