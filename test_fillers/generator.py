import random

import mimesis
from django.contrib.auth.models import User
from django.db.models import Q
from mimesis import Person
from mimesis.enums import Gender
from mimesis.locales import Locale

from src.accounts.models import Profile, ExecutorOffer, Specialization, Status
from src.projects.models import Project
from src.tests.models import BelbinTest, MBTITest, LSQTest

username_whitelist = [
    'dm1tr',
]

text = mimesis.Text(Locale.RU)
address = mimesis.Address(Locale.RU)
person = Person(Locale.RU)


def generate_users(n=1):
    for i in range(n):
        user = User.objects.create(**{'username': person.username(
            drange=(1, 2100)),
            'email': person.email()})
        user.set_password('worldhello')
        user.profile.belbin.set(list(random.sample(list(range(1, 8)),
                                                   random.randint(0, 2))))

        mx = Specialization.objects.last().id
        mn = Specialization.objects.first().id
        user.profile.specialization.set(
            list(random.sample(list(range(mn, mx + 1)), random.randint(0, 5))))

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

            mx = BelbinTest.objects.last().id
            mn = BelbinTest.objects.first().id
            project.required_belbin.set(
                list(random.sample(list(range(mn, mx + 1)),
                                   random.randint(1, 7))))

            mx = Specialization.objects.last().id
            mn = Specialization.objects.first().id
            a = list(
                random.sample(list(range(mn, mx + 1)), random.randint(1, 20)))
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


def generate_belbin_roles():
    roles = [
        'Педант',
        'Душа команды',
        'Аналитик-стратег',
        'Исследователь ресурсов',
        'Генератор идей',
        'Мотиватор',
        'Координатор',
        'Исполнитель'
    ]

    for role in roles:
        BelbinTest.objects.create(role=role)


def generate_mbti_roles():
    roles = [
        'Иррационал',
        'Рационал',
        'Логик',
        'Этик',
        'Интуит',
        'Сенсорик',
        'Интроверт',
        'Экстраверт'
    ]

    for role in roles:
        MBTITest.objects.create(role=role)


def generate_lsq_roles():
    roles = [
        'Рефлексирующий',
        'Прагматик',
        'Теоретик',
        'Деятель',
    ]

    for role in roles:
        LSQTest.objects.create(role=role)


def generate_specializations():
    spec_list = {'Диспетчер', 'Контроль качества', 'Корректор, ретушер',
                 'Администрирование', 'Закупки, Снабжение',
                 'Кассовое обслуживание, инкассация', 'Автомобильный бизнес',
                 'Антимонопольное право', 'Компенсации и льготы',
                 'Дизайн/Оформление',
                 'Языки', 'Продажа', 'Сиделка', 'Маркшейдер',
                 'Легкая промышленность',
                 'Химия', 'CIPA', 'Реинжиниринг бизнес процессов',
                 'Гражданская авиация',
                 'Налоговое право', 'Верстальщик', 'Машинист производства',
                 'Правительство', 'Парикмахер', 'Главный агроном',
                 'Ипотека, Ипотечное кредитование', 'Ногтевой сервис',
                 'Станки, Тяжелое оборудование', 'Internet, E-Commerce',
                 'Медицинское оборудование', 'Массажист', 'Перестрахование',
                 'Кассир, Инкассатор', 'Агент', 'Арт директор', 'Девелопер',
                 'Законотворчество', 'Помощник по хозяйству, Управляющий',
                 'Администратор баз данных',
                 'Менеджер по сервису - сетевые и телекоммуникационные технологии',
                 'Атомная энергетика', 'Железнодорожные перевозки',
                 'Страхование недвижимости', 'Телевидение', 'Автослесарь',
                 'Аналитик',
                 'Банковское ПО', 'Авиационная промышленность',
                 'Информатика, Информационные системы', 'Курьер', 'Лаборант',
                 'Воспитатель, Гувернантка/гувернёр, Няня', 'Фотография',
                 'Управление персоналом', 'Корпоративные финансы',
                 'Сервисное обслуживание', 'Повар', 'CTO, CIO, Директор по IT',
                 'Гид, Экскурсовод', 'Автомойщик',
                 'Отопление, вентиляция и кондиционирование',
                 'Деревообработка, Лесная промышленность',
                 'Компьютерные программы',
                 'Интернет-маркетинг', 'Бурение', 'Главный инженер',
                 'Бухгалтер-калькулятор', 'Коммерческий Банк', 'Журналистика',
                 'Оптика',
                 'Морские/Речные перевозки', 'Автозапчасти',
                 'Административный персонал',
                 'Добыча сырья', 'Актуарий', 'Машинист экскаватора',
                 'Бюджетирование и планирование', 'Консультант', 'Лифтер',
                 'Руководитель направления', 'Рабочий персонал',
                 'Private Banking',
                 'Комплексное страхование юридических лиц', 'Косметология',
                 'Синхронный перевод', 'Compliance', 'Письменный перевод',
                 'Секретарь',
                 'Игровое ПО', 'Анимация', 'Гостиницы, Магазины', 'Логистика',
                 'Дизайнер',
                 'PR, Маркетинговые коммуникации', 'Маркетинг, Реклама, PR',
                 'Консультирование', 'Архивист', 'Арт-директор', 'Web мастер',
                 'Издательская деятельность', 'Механик', 'Развитие персонала',
                 'Интеллектуальная собственность', 'Недвижимость', 'Стратегия',
                 'Казначейство', 'Антикризисное управление',
                 'Размещение, Обслуживание гостей',
                 'Инсталляция и настройка оборудования',
                 'Охранник', 'Главный механик',
                 'Внутренние операции (Back Office)',
                 'Оператор станков', 'Пожарная безопасность', 'Персонал кухни',
                 'Forex',
                 'Экономическая и информационная безопасность',
                 'Продукты питания',
                 'Жестянщик', 'Бизнес-авиация', 'Автомобили, Запчасти',
                 'FMCG, Товары народного потребления',
                 'Инвестиционная компания',
                 'Информационные технологии', 'Страхование ответственности',
                 'Корпоративное право', 'Руда', 'Производство',
                 'Закупки и снабжение',
                 'Контент', 'Архивариус',
                 'Организация туристических продуктов',
                 'Дошкольное образование', 'Преподавание', 'Автокредитование',
                 'Ввод данных', 'Медицинское страхование', 'Ассистент',
                 'Начальный уровень, Мало опыта', 'ЖКХ',
                 'Информационные технологии, Интернет, Мультимедиа',
                 'Зоотехник',
                 'Искусство, Развлечения, Масс-медиа', 'Врач-эксперт',
                 'Управление закупками', 'Консалтинг, Аутсорсинг',
                 'Конструктор',
                 'Персональный водитель', 'Дефектолог, Логопед',
                 'Сотрудник полиции/ГИБДД',
                 'Менеджер по работе с клиентами', 'Бренд-менеджмент',
                 'Общественный транспорт', 'Грузчик',
                 'Компьютерная безопасность',
                 'Компьютерная техника', 'Аудит, Внутренний контроль',
                 'Дизайн, графика, живопись', 'Имущественная безопасность',
                 'Управление проектами', 'Уборщица/уборщик',
                 'Автомобильная промышленность', 'Гардеробщик', 'Монтажник',
                 'Репетитор',
                 'Нефть', 'Ресепшен', 'Наука, Образование',
                 'Менеджмент продукта (Product manager)', 'CRM системы',
                 'Прокат, лизинг',
                 'Науки о Земле', 'Дистрибуция', 'Тренерский состав',
                 'МСФО, IFRS', 'Газ',
                 'Дорожные рабочие', 'Денежный рынок (money market)',
                 'Инкассатор',
                 'Управление предприятием', 'Казино и игорный бизнес',
                 'Инженер, Мясо- и птицепереработка', 'Сомелье',
                 'Добыча cырья',
                 'Автострахование', 'Кино', 'Страхование жизни',
                 'Последовательный перевод', 'Строительные материалы',
                 'Web инженер',
                 'Медицинский представитель', 'Сертификация', 'Автоперевозки',
                 'Официант, Бармен', 'Бюджетирование', 'Благотворительность',
                 'Мебель',
                 'ACCA', 'Землеустройство', 'Страхование бизнеса',
                 'Многоуровневый маркетинг',
                 'Менеджер по сервису - промышленное оборудование', 'Тренинги',
                 'Казначейство, Управление ликвидностью', 'Налоги',
                 'Комплектовщик, Укладчик-упаковщик', 'Валютный контроль',
                 'Учет кадров',
                 'Производство, Технологии', 'Радио', 'Продажи',
                 'Кредитный контроль',
                 'Автожестянщик', 'Below The Line (BTL)', 'Дворник, Уборщик',
                 'Лекарственные препараты', 'Интернет', 'Акции, Ценные бумаги',
                 'Кладовщик', 'Оценка', 'Тендеры', 'Экономика, Менеджмент',
                 'АХО',
                 'Личная безопасность', 'ВЭД', 'Дилерские сети', 'Математика',
                 'Другое',
                 'Муниципалитет', 'Сервисный инженер', 'GAAP',
                 'Проектирование, Архитектура', 'Наладчик', 'Шины, Диски',
                 'Руководитель СБ', 'Аудит', 'Бухгалтер', 'Музыка', 'Провизор',
                 'Договорное право', 'Авиабилеты', 'Общественные организации',
                 'Клинические исследования', 'Мерчендайзинг',
                 'Инженерные науки',
                 'Основные средства', 'Страхование',
                 'Комплексное страхование физических лиц',
                 'Медицина, Фармацевтика',
                 'Фармацевтика', 'Клининговые услуги', 'Биотехнологии',
                 'Системы видеонаблюдения', 'Алкоголь', 'Лечащий врач',
                 'Геологоразведка',
                 'Бронирование', 'Товары для бизнеса', 'Закупки',
                 'Геодезия и картография',
                 'Администрация', 'Организационное консультирование',
                 'Сотрудник call-центра', 'Краснодеревщик', 'Авиаперевозки',
                 'Кейтеринг',
                 'Мода', 'Военнослужащий',
                 'домработница/домработник, Горничная', 'Уголь',
                 'Организация встреч, Конференций', 'Рекрутмент',
                 'Производство, Технология', 'Водитель', 'ГСМ, нефть, бензин',
                 'Физика',
                 'Контейнерные перевозки', 'НИИ', 'Инженер',
                 'Литературная, Редакторская деятельность',
                 'Взыскание задолженности, Коллекторская деятельность',
                 'Продажа туристических услуг', 'Персональный ассистент',
                 'Гуманитарные науки', 'Маркетинг', 'Маляр', 'Инвестиции',
                 'Банковское право', 'Строительство, Недвижимость',
                 'Земельное право',
                 'Инженер, Производство и переработка зерновых', 'Арбитраж',
                 'Бухгалтерия',
                 'Копирайтер', 'Управленческое консультирование',
                 'Андеррайтер',
                 'Младший и средний медперсонал', 'Исследования рынка',
                 'Бытовая техника',
                 'Водоснабжение и канализация', 'Адвокат', 'Делопроизводство',
                 'Банкеты',
                 'Жилье', 'Управление практикой', 'Медицинский советник',
                 'Международное право', 'Ветеринария', 'Нежилые помещения',
                 'Металлопрокат'}

    for spec in spec_list:
        Specialization.objects.create(name=spec)


def generate_statuses():
    statuses = ['Приглашен', 'Ожидает']

    for status in statuses:
        Status.objects.create(value=status)


def generate_all():
    generate_specializations()
    generate_mbti_roles()
    generate_lsq_roles()
    generate_belbin_roles()
    generate_statuses()
    generate_users(100)
    generate_projects()
    generate_executor_offers()
