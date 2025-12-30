from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Section, Material, Test, CodingProblem, Submission
from .forms import SubmissionForm
from django.db.models import Q
import subprocess
import sys


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
        user = self.request.user

        # Получаем все разделы с материалами, их блоками и тестами
        sections = course.sections.prefetch_related(
            'materials__blocks', 'materials__coding_problems', 'tests'
        ).all()

        # Обработка вариантов ответов для тестов
        for section in sections:
            section.materials_list = section.materials.all()
            for material in section.materials_list:
                material.problems = material.coding_problems.all()
                if user.is_authenticated:
                    for problem in material.problems:
                        problem.user_submission = Submission.objects.filter(problem=problem, student=user).first()

            section.tests_list = section.tests.all()
            for test in section.tests_list:
                test.answer_choices = test.answer_choices.split(',')

        # Проверка прогресса (студент не может видеть следующие разделы без решения задач)
        if user.is_authenticated:
            all_accepted = True
            for section in sections:
                section.locked = not all_accepted
                
                # Проверяем обязательные задачи в текущем разделе для открытия следующего
                for material in section.materials_list:
                    for problem in material.problems:
                        if problem.is_required:
                            if not problem.user_submission or problem.user_submission.status != 'ACCEPTED':
                                all_accepted = False
                                break
                    if not all_accepted: break
                if not all_accepted:
                    # Помечаем заблокированные разделы после первого непройденного
                    pass

        context['sections'] = sections
        return context

def submit_solution(request, problem_id):
    problem = get_object_or_404(CodingProblem, id=problem_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            submission.student = request.user
            
            # Simple Variant B implementation
            try:
                # Security note: In production use a sandbox like Docker
                code = submission.code
                result = subprocess.run(
                    [sys.executable, "-c", code],
                    input=problem.input_data,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                output = result.stdout.strip()
                if output == problem.expected_output.strip():
                    submission.status = 'ACCEPTED'
                else:
                    submission.status = 'FAILED'
                    submission.feedback = f"Expected: {problem.expected_output}\nGot: {output}\nError: {result.stderr}"
            except subprocess.TimeoutExpired:
                submission.status = 'FAILED'
                submission.feedback = "Execution timeout"
            except Exception as e:
                submission.status = 'FAILED'
                submission.feedback = str(e)
                
            submission.save()
    return redirect('course_detail', pk=problem.material.section.course.id)

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
