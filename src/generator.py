import random

from django.contrib.auth.models import User

from src.accounts.models import Profile, ExecutorOffer
from src.projects.models import Project


def generate_users(start, n=1):
    for i in range(start, start + n):
        user = User.objects.create(**{'username': f't{i}',
                                      'email': f't{i}@mail.ru'})
        user.set_password('worldhello')
        user.profile.belbin.set(list(random.sample(list(range(1, 8)),
                                                   random.randint(0, 2))))
        user.profile.specialization.set(
            list(random.sample(list(range(650, 800)), random.randint(0, 5))))
        user.save()


def generate_projects(start, n=1):
    for i in range(start, start + n):
        project = Project.objects.create(
            owner=Profile.objects.get(user__username=f't{i}'),
            title=f'project_t{i}',
            description=f'desc for t{i}',
            vacant=random.randint(0, 20),
        )

        project.required_belbin.set(
            list(random.sample(list(range(1, 8)), random.randint(1, 7))))

        a = list(random.sample(list(range(650, 800)), random.randint(1, 20)))
        project.required_specialization.set(a)


def generate_executor_offers(start, n=1):
    for i in range(start, start + n):
        ExecutorOffer.objects.create(
            profile=Profile.objects.get(user__username=f't{i}'),
            description=f'offer of t{i} desc',
            work_hours=random.randint(3, 100)
        )
