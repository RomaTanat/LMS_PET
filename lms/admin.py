from django.contrib import admin
from .models import Course, Section, Material, Test

# Инлайн форма для разделов
class SectionInline(admin.TabularInline):
    model = Section
    extra = 1  # Показывать одну пустую строку для добавления нового раздела
    fields = ['title', 'order']  # Поля для редактирования

# Инлайн форма для материалов
class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1  # Показывать одну пустую строку для добавления нового материала
    fields = ['title', 'content', 'file', 'link']  # Поля для редактирования
    # Указываем поле, которое связывает материал с разделом
    fk_name = 'section'

# Инлайн форма для тестов
class TestInline(admin.TabularInline):
    model = Test
    extra = 1  # Показывать одну пустую строку для добавления нового теста
    fields = ['question', 'correct_answer', 'answer_choices']  # Поля для редактирования
    # Указываем поле, которое связывает тест с разделом
    fk_name = 'section'

# Админка для модели Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ['title', 'author__username']  # Поиск по названию и имени автора
    inlines = [SectionInline]  # Добавляем инлайн-формы для редактирования связанных разделов

# Регистрируем модель в админке
admin.site.register(Course, CourseAdmin)

# Регистрируем модели для админки
admin.site.register(Section)
admin.site.register(Material)
admin.site.register(Test)
