from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render
from .models import Course, Section, Material, Test
from django.db.models import Q
from django.views.generic import ListView
from .models import Course


#список курсов
class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return queryset




# Детальная страница курса
class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object

        # Получаем все разделы с материалами и тестами
        sections = course.sections.prefetch_related(
            'materials', 'tests'
        ).all()

        # Обработка вариантов ответов для тестов
        for section in sections:
            section.materials = section.materials.all()
            section.tests = section.tests.all()
            for test in section.tests:
                test.answer_choices = test.answer_choices.split(',')

        context['sections'] = sections
        return context

# Профиль пользователя
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"  # Убедитесь, что у вас есть этот шаблон

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Передаем текущего пользователя в шаблон
        return context

# Главная страница
def home(request):
    return render(request, "home.html")

# Страница "О нас"
def about(request):
    return render(request, "about.html")
