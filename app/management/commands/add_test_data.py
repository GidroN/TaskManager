from django.core.management.base import BaseCommand
from app.models import User, Group, Task
from app.utils import JsonImport
from template_hub.models import Template, Comment


class Command(BaseCommand):
    help = 'Adds test data to the database'

    def handle(self, *args, **options):
        # Create Users
        admin = User(username='admin', email='admin@email.com', is_superuser=True, is_staff=True)
        admin.set_password('admin')
        admin.save()

        user1 = User(username='user1', email='user1email1@email.com')
        user1.set_password('user')
        user1.save()

        user2 = User(username='user2', email='user2email2@email.com')
        user2.set_password('user')
        user2.save()

        users = [admin, user1, user2]

        # Create Group and Tasks using import
        data = {
            'Работа': [{'name': 'Сделать макет', 'description': ''},
                       {'name': 'Продумать БД', 'description': ''}],
            'Домашний дела': [{'name': 'Сварить суп', 'description': ''},
                              {'name': 'Помыть полы', 'description': ''}],
            'Учеба': [{'name': 'Сделать презентацию', 'description': ''},
                      {'name': 'Подготовить доклад', 'description': ''}]
        }

        for user in users:
            importer = JsonImport(data, user)
            importer.import_data()

        # Create Templates
        template1 = Template.objects.create(name='Мотивация учебы', file='app/management/fixtures/learn_motivation.json',
                                            user=user1, description='Этот шаблон помогает в управлении личными '
                                                                    'финансами, планировании бюджета и достижении '
                                                                    'финансовых целей.')

        template2 = Template.objects.create(name='Здоровый образ жизни', file='app/management/fixtures/healthy_life.json',
                                            user=user1, description='Идеален для профессионалов, стремящихся '
                                                                    'оптимизировать свою рабочую эффективность и '
                                                                    'достигать лучших результатов.')

        template3 = Template.objects.create(name='Организация рабочего процесса',
                                            file='app/management/fixtures/work_life_balance.json', user=user2,
                                            description='Идеален для профессионалов, стремящихся оптимизировать свою '
                                                        'рабочую эффективность и достигать лучших результатов.')

        template4 = Template.objects.create(name='Управление финансами', file='app/management/fixtures/money.json', user=user2,
                                            description='Этот шаблон создан для студентов, желающих улучшить свою '
                                                        'учебную мотивацию и организованность.')

        # Create Comments for Templates
        Comment.objects.create(template=template1, user=user2,
                               text='Хороший шаблон для студентов, но было бы здорово добавить еще советы по управлению'
                                    'временем во время сессии. В остальном, отличная помощь для организации учебы!')

        Comment.objects.create(template=template2, user=user2,
                               text='Прекрасный шаблон для тех, кто хочет начать вести здоровый образ жизни. Особенно '
                                    'понравилась группа с питанием, это помогло мне организовать мои ежедневные приемы '
                                    'пищи')

        Comment.objects.create(template=template3, user=user1,
                               text='Использую этот шаблон уже две недели и чувствую, что стал продуктивнее. Однако, '
                                    'некоторые задачи кажутся излишними, возможно стоит упростить раздел про снижение '
                                    'стресса.')

        Comment.objects.create(template=template4, user=user1,
                               text='Этот шаблон помог мне лучше понять мои финансы, но хотелось бы видеть больше '
                                    'инструментов для автоматизации отслеживания расходов. Вручную это занимает много '
                                    'времени.')
