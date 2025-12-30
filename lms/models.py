from django.contrib.auth.models import AbstractUser
from django.db import models
from django.views.generic import DetailView


from django.template.defaultfilters import register

@register.filter
def split(value, arg):
    return value.split(arg)

# Модель пользователя
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    enrolled_courses = models.ManyToManyField('Course', blank=True, related_name='courses_enrolled', verbose_name="Записанные курсы")

    def __str__(self):
        return self.username


# Модель курса
class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses", verbose_name="Автор")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        print(f"Открыт курс: {course}")  # Вывод в консоль сервера

        sections = course.sections.prefetch_related('materials', 'tests').all()
        for section in sections:
            section.materials = section.materials.all()
            section.tests = section.tests.all()
            for test in section.tests:
                test.answer_choices = test.answer_choices.split(',')
        context['sections'] = sections
        return context


# Модель раздела (для структуры курса)
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections", verbose_name="Курс")
    title = models.CharField(max_length=255, verbose_name="Название раздела")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок раздела")

    class Meta:
        ordering = ['order']  # Сортируем разделы по порядку

    def __str__(self):
        return self.title


# Модель материала (файлы, видео, ссылки)
class Material(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="materials", verbose_name="Раздел")
    title = models.CharField(max_length=255, verbose_name="Название материала")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


    # Блоки контента для материала
class ContentBlock(models.Model):
    BLOCK_TYPES = [
        ('TEXT', 'Текст'),
        ('VIDEO', 'Видео'),
        ('CODE_SNIPPET', 'Пример кода'),
        ('FILE', 'Файл'),
        ('PRACTICE', 'Практика кода'),
        ('TASK', 'Задача'),
    ]
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="blocks", verbose_name="Материал")
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES, default='TEXT', verbose_name="Тип блока")
    content = models.TextField(blank=True, null=True, verbose_name="Текстовый контент/Код")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    file = models.FileField(upload_to="materials/blocks/", blank=True, null=True, verbose_name="Файл")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    # Дополнительные поля для практики и задач
    metadata = models.JSONField(blank=True, null=True, verbose_name="Метаданные (LeetCode/Jira style)")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.block_type} block for {self.material.title}"


# Модель теста (вопросы и ответы)
class Test(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="tests", verbose_name="Раздел")
    question = models.CharField(max_length=512, verbose_name="Вопрос")
    correct_answer = models.CharField(max_length=255, verbose_name="Правильный ответ")
    answer_choices = models.TextField(verbose_name="Варианты ответов", help_text="Перечислите варианты через запятую")

    def __str__(self):
        return self.question


# Задачи по программированию (LeetCode-style)
class CodingProblem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    input_data = models.TextField(verbose_name="Входные данные (тест)")
    expected_output = models.TextField(verbose_name="Ожидаемый результат")
    hints = models.TextField(blank=True, null=True, verbose_name="Подсказки")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="coding_problems", verbose_name="Урок/Материал")
    is_required = models.BooleanField(default=True, verbose_name="Обязательная для прогресса")

    def __str__(self):
        return self.title

# Решения студентов
class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'На проверке'),
        ('ACCEPTED', 'Принято'),
        ('REJECTED', 'На доработку'),
        ('FAILED', 'Ошибка выполнения'),
    ]
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField(verbose_name="Код решения")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    feedback = models.TextField(blank=True, null=True, verbose_name="Отзыв преподавателя")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.student.username} for {self.problem.title}"

# Управление задачами (Jira-lite)
class PersonalTask(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_assigned", verbose_name="Студент")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_created", verbose_name="Ментор")
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO', verbose_name="Статус")
    deadline = models.DateTimeField(blank=True, null=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.student.username})"

class TaskComment(models.Model):
    task = models.ForeignKey(PersonalTask, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"

# Профиль студента с геймификацией
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    level = models.IntegerField(default=1, verbose_name="Уровень")
    current_xp = models.IntegerField(default=0, verbose_name="Опыт на уровне")
    total_xp = models.IntegerField(default=0, verbose_name="Всего опыта")
    streak_days = models.IntegerField(default=0, verbose_name="Дней подряд")
    last_activity_date = models.DateField(null=True, blank=True, verbose_name="Дата последней активности")

    def add_xp(self, amount):
        self.current_xp += amount
        self.total_xp += amount
        
        # Геометрическая прогрессия: опыт для следующего уровня = 100 * (1.5 ** (level - 1))
        xp_needed = int(100 * (1.5 ** (self.level - 1)))
        
        while self.current_xp >= xp_needed:
            self.current_xp -= xp_needed
            self.level += 1
            xp_needed = int(100 * (1.5 ** (self.level - 1)))
        
        self.save()

    def update_streak(self):
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.last_activity_date == today:
            return
            
        if self.last_activity_date == today - timezone.timedelta(days=1):
            self.streak_days += 1
        else:
            self.streak_days = 1
            
        self.last_activity_date = today
        self.save()

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    if hasattr(instance, 'student_profile'):
        instance.student_profile.save()

# Модель достижений (Achievements)
class Achievement(models.Model):
    """Achievement/Badge that users can earn"""
    CRITERIA_TYPES = [
        ('course_count', 'Количество курсов'),
        ('test_score', 'Результат теста'),
        ('login_streak', 'Серия входов'),
        ('material_views', 'Просмотр материалов'),
        ('course_completion', 'Завершение курса'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Название достижения")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=50, default='🏆', verbose_name="Иконка")
    criteria_type = models.CharField(max_length=50, choices=CRITERIA_TYPES, verbose_name="Тип критерия")
    criteria_value = models.IntegerField(verbose_name="Значение критерия")
    points = models.IntegerField(default=10, verbose_name="Очки")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"
    
    def __str__(self):
        return f"{self.icon} {self.name}"


# Модель достижений пользователя
class UserAchievement(models.Model):
    """User's earned achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements', verbose_name="Пользователь")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, verbose_name="Достижение")
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name="Получено")
    progress = models.IntegerField(default=0, verbose_name="Прогресс (0-100)")
    
    class Meta:
        verbose_name = "Достижение пользователя"
        verbose_name_plural = "Достижения пользователей"
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

