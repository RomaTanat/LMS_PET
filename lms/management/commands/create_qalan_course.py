
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms.models import Course, Section, Material, ContentBlock, CodingProblem

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates the Qalan "Programming as Mathematics" course structure'

    def handle(self, *args, **options):
        # 1. Ensure Author exists
        author, created = User.objects.get_or_create(
            username='qalan_admin',
            defaults={'email': 'admin@qalan.kz', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            author.set_password('qalan_password')
            author.save()
            self.stdout.write(self.style.SUCCESS('Created admin user "qalan_admin"'))

        # 2. Create Course
        course_title = "Программирование как математика в Қалан"
        description = """
        Методы:
        - Постоянное повторение
        - Напоминание трехкратное
        - Для детей интересующихся разработкой
        - Менторство и онлайн поддержка
        - Теория + тесты + индивидуальное сопровождение
        - ИИ поддержка

        Целевая аудитория: жасөспірімдер, балалар, кез келген айти энтузиаст
        """

        course, created = Course.objects.get_or_create(
            title=course_title,
            defaults={
                'description': description,
                'author': author
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course "{course_title}"'))
        else:
            self.stdout.write(self.style.WARNING(f'Course "{course_title}" already exists. Updating sections...'))

        # 3. Define Structure
        structure = [
            {
                "title": "Введение",
                "materials": [
                    {"title": "Добро пожаловать в Qalan", "type": "TEXT", "content": "Введение в платформу и методологию обучения."},
                ]
            },
            {
                "title": "Вся теория и синтаксис языков",
                "materials": [
                    {"title": "Основы синтаксиса Python", "type": "TEXT", "content": "Переменные, циклы, условия."},
                    {"title": "Синтаксис JavaScript", "type": "TEXT", "content": "Основы JS для веб-разработки."},
                ]
            },
            {
                "title": "Отдельные задачи и тесты по темам",
                "materials": [
                    {"title": "Задачи на циклы", "type": "PRACTICE", "content": "Решите задачи на for и while."},
                    {"title": "Тест по типам данных", "type": "TEXT", "content": "Пройдите тест (ссылка на тест)."},
                ]
            },
            {
                "title": "Ручная работа пет проекты",
                "materials": [
                    {"title": "Идея вашего первого проекта", "type": "TEXT", "content": "Как выбрать идею для пет-проекта."},
                    {"title": "Планирование", "type": "TEXT", "content": "Этапы разработки."},
                ]
            },
            {
                "title": "Дизайн и верстка",
                "materials": [
                    {"title": "Основы HTML/CSS", "type": "VIDEO", "video_url": "https://www.youtube.com/watch?v=example", "content": "Видео урок по верстке."},
                    {"title": "Адаптивный дизайн", "type": "TEXT", "content": "Media queries и Flexbox."},
                ]
            },
            {
                "title": "Теория про инфраструктуру",
                "materials": [
                    {"title": "Железо и ОС", "type": "TEXT", "content": "Как работает компьютер, память, процессор."},
                    {"title": "Взаимосвязи и сети", "type": "TEXT", "content": "Как работает Интернет, HTTP, DNS."},
                    {"title": "Оптимизация", "type": "TEXT", "content": "Основы алгоритмической сложности."},
                ]
            },
            {
                "title": "Первая теория по логике",
                "materials": [
                    {"title": "Булева алгебра", "type": "TEXT", "content": "True, False, AND, OR, NOT."},
                    {"title": "Алгоритмическое мышление", "type": "TEXT", "content": "Блок-схемы и псевдокод."},
                ]
            },
            {
                "title": "Тестовые кейсы реализации логики",
                "materials": [
                    {"title": "Пишем тесты", "type": "CODE_SNIPPET", "content": "assert sum([1, 2]) == 3"},
                ]
            },
            {
                "title": "Пет проект реализации логики",
                "materials": [
                    {"title": "Проект: Калькулятор логики", "type": "TASK", "content": "Создайте программу, решающую логические выражения."},
                ]
            },
            {
                "title": "Чат боты и Апи",
                "materials": [
                    {"title": "Что такое API?", "type": "TEXT", "content": "REST, JSON, запросы."},
                    {"title": "Создаем эхо-бота", "type": "CODE_SNIPPET", "content": "Код простого бота."},
                    {"title": "Платформы и объединение API", "type": "TEXT", "content": "Интеграция разных сервисов."},
                ]
            },
            {
                "title": "Реализация на любых языках",
                "materials": [
                    {"title": "Объяснение систем и шаблонов", "type": "TEXT", "content": "MVC, MVVM, Singleton и другие паттерны."},
                    {"title": "Теория + практика разных языков", "type": "TEXT", "content": "Сравнение реализации на Python, JS, C++."},
                ]
            },
            {
                "title": "Менторство и Деплой",
                "materials": [
                    {"title": "Как загрузить проект на сервер", "type": "TEXT", "content": "SSH, Linux, Nginx."},
                    {"title": "CI/CD основы", "type": "TEXT", "content": "Автоматизация деплоя."},
                    {"title": "Публикация проекта", "type": "TEXT", "content": "Где и как показать свой проект миру."},
                ]
            }
        ]

        # 4. Populate Database
        for i, section_data in enumerate(structure):
            section, _ = Section.objects.get_or_create(
                course=course,
                title=section_data['title'],
                defaults={'order': i + 1}
            )

            for j, mat_data in enumerate(section_data['materials']):
                material, _ = Material.objects.get_or_create(
                    section=section,
                    title=mat_data['title'],
                    defaults={'order': j + 1}
                )

                # Create Content Block if material was just created (or strictly check if blocks exist)
                if not material.blocks.exists():
                    ContentBlock.objects.create(
                        material=material,
                        block_type=mat_data.get('type', 'TEXT'),
                        content=mat_data.get('content', ''),
                        video_url=mat_data.get('video_url', ''),
                        order=1
                    )

        self.stdout.write(self.style.SUCCESS('Successfully populated course structure!'))
