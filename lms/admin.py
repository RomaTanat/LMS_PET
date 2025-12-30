from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Course, Section, Material, Test, ContentBlock, User, StudentProfile, Achievement, UserAchievement, CodingProblem, Submission, PersonalTask, TaskComment, Notification

# Инлайн форма для блоков контента
class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    extra = 1
    fields = ['block_type', 'content', 'video_url', 'file', 'order']
    fk_name = 'material'

# Инлайн форма для разделов
class SectionInline(admin.TabularInline):
    model = Section
    extra = 1  # Показывать одну пустую строку для добавления нового раздела
    fields = ['title', 'order']  # Поля для редактирования

# Инлайн форма для материалов
class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1  # Показывать одну пустую строку для добавления нового материала
    fields = ['title', 'order']  # Поля для редактирования
    show_change_link = True # Allow editing material details (including ContentBlocks)
    fk_name = 'section'

# Инлайн форма для тестов
class TestInline(admin.TabularInline):
    model = Test
    extra = 1  # Показывать одну пустую строку для добавления нового теста
    fields = ['question', 'correct_answer', 'answer_choices']  # Поля для редактирования
    fk_name = 'section'

# Админка для модели Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ['title', 'author__username']  # Поиск по названию и имени автора
    inlines = [SectionInline]  # Добавляем инлайн-формы для редактирования связанных разделов

# Админка для модели Section
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ['title', 'course__title']
    inlines = [MaterialInline, TestInline]

# Админка для модели Material
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section__course', 'section')
    search_fields = ['title', 'section__title']
    inlines = [ContentBlockInline]

# Админка для модели User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# Регистрируем модели в админке
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Test)
admin.site.register(ContentBlock)
admin.site.register(StudentProfile)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(CodingProblem)
admin.site.register(Submission)
admin.site.register(PersonalTask)
admin.site.register(TaskComment)
admin.site.register(Notification)
