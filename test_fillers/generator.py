import random

import mimesis
from django.contrib.auth.models import User
from django.db.models import Q
from mimesis import Person
from mimesis.enums import Gender
from mimesis.locales import Locale

from src.accounts.models import Profile, ExecutorOffer
from src.projects.models import Project

username_whitelist = [
    'dm1tr',
]

text = mimesis.Text(Locale.RU)
address = mimesis.Address(Locale.RU)
person = Person(Locale.RU)


def generate_users(n=1):
    for i in range(n):
        user = User.objects.create(**{'username': person.username(drange=(1,
                                                                          2100)),
                                      'email': person.email()}
                                   )
        user.set_password('worldhello')
        user.profile.belbin.set(list(random.sample(list(range(1, 8)),
                                                   random.randint(0, 2))))
        user.profile.specialization.set(
            list(random.sample(list(range(650, 800)), random.randint(0, 5))))

        if random.randint(0, 1) == 0:
            user.profile.is_male = True
            user.first_name = person.name(gender=Gender.MALE)
            user.last_name = person.last_name(gender=Gender.MALE)
        else:
            user.profile.is_male = False
            user.first_name = person.name(gender=Gender.FEMALE)
            user.last_name = person.last_name(gender=Gender.FEMALE)

        user.profile.city = address.city()
        user.profile.description = text.text(random.randint(1, 5))
        user.profile.age = random.randint(20, 77)

        if random.randint(0, 1) > 0:
            user.profile.remote = random.randint(1, 3)

        user.profile.save()
        user.save()


def generate_projects():
    for profile in Profile.objects.filter(
            ~Q(user__username__in=username_whitelist)):
        if random.randint(0, 10) < 4:
            project = Project.objects.create(
                owner=profile,
                title=text.word() + ' ' + text.word(),
                description=text.text(random.randint(1, 5)),
                vacant=random.randint(0, 20),
                city=address.city(),
            )

            if random.randint(0, 1) > 0:
                project.online = True if random.randint(0, 1) > 0 else False

            project.required_belbin.set(
                list(random.sample(list(range(1, 8)), random.randint(1, 7))))

            a = list(
                random.sample(list(range(650, 800)), random.randint(1, 20)))
            project.required_specialization.set(a)


def generate_executor_offers():
    for profile in Profile.objects.filter(
            ~Q(user__username__in=username_whitelist)):
        ExecutorOffer.objects.create(
            profile=profile,
            description=text.text(random.randint(1, 5)),
            work_hours=random.randint(3, 100),
            salary=random.randint(10_000, 1_000_000),
        )
