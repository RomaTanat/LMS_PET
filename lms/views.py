from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Section, Material, Test, CodingProblem, Submission
from .forms import SubmissionForm, ProfileUpdateForm
from django.db.models import Q
from django.urls import reverse_lazy
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

from .services import analyze_code_submission
from .gamification import process_submission_rewards, purchase_item

def submit_solution(request, problem_id):
    problem = get_object_or_404(CodingProblem, id=problem_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            submission.student = request.user
            submission.save()
            
            # Запускаем фоновый анализ
            analyze_code_submission(submission)
            
            # Начисление наград (XP, Coins, Achievements)
            if submission.status == 'ACCEPTED':
                if hasattr(request.user, 'student_profile'):
                    request.user.student_profile.update_streak()
                    process_submission_rewards(submission)
                
            submission.save()
    return redirect('course_detail', pk=problem.material.section.course.id)

from .models import Course, Section, Material, CodingProblem, Submission, PersonalTask, TaskComment, Notification, User, ShopItem, StudentProfile, Clan
from django.contrib import messages
from django.db import transaction

# --- Магазин ---
class ShopView(LoginRequiredMixin, ListView):
    model = ShopItem
    template_name = "gamification/shop.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем список купленных ID, чтобы отключить кнопку "Купить"
        purchased_ids = self.request.user.student_profile.inventory.values_list('item_id', flat=True)
        context['purchased_ids'] = purchased_ids
        return context

@transaction.atomic
def buy_item_view(request, item_id):
    if request.method == 'POST':
        success, message = purchase_item(request.user, item_id)
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    return redirect('shop')

# --- Лидерборд ---
class LeaderboardView(LoginRequiredMixin, ListView):
    model = StudentProfile
    template_name = "gamification/leaderboard.html"
    context_object_name = "profiles"
    paginate_by = 20

    def get_queryset(self):
        return StudentProfile.objects.select_related('user').order_by('-weekly_xp')

# --- Кланы ---
class ClanListView(LoginRequiredMixin, ListView):
    model = Clan
    template_name = "gamification/clan_list.html"
    context_object_name = "clans"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_clan'] = self.request.user.student_profile.clan
        return context

def create_clan(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            if Clan.objects.filter(name=name).exists():
                messages.error(request, "Клан с таким именем уже существует.")
            else:
                clan = Clan.objects.create(name=name, description=description, leader=request.user)
                profile = request.user.student_profile
                profile.clan = clan
                profile.save()
                messages.success(request, f"Клан {name} создан!")
                return redirect('clan_list')
    return redirect('clan_list')

def join_clan(request, clan_id):
    clan = get_object_or_404(Clan, id=clan_id)
    profile = request.user.student_profile
    profile.clan = clan
    profile.save()
    messages.success(request, f"Вы вступили в клан {clan.name}!")
    return redirect('clan_list')

def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    if notification.link:
        return redirect(notification.link)
    return redirect('user_profile')

def update_task_status(request, task_id):
    task = get_object_or_404(PersonalTask, id=task_id)
    if request.user == task.student or request.user == task.teacher:
        new_status = request.POST.get('status')
        if new_status in dict(PersonalTask.STATUS_CHOICES):
            task.status = new_status
            task.save()
    return redirect('user_profile')

def add_task_comment(request, task_id):
    task = get_object_or_404(PersonalTask, id=task_id)
    if request.method == 'POST' and (request.user == task.student or request.user == task.teacher):
        content = request.POST.get('content')
        if content:
            TaskComment.objects.create(task=task, author=request.user, content=content)
    return redirect('user_profile')

# Профиль пользователя
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['assigned_tasks'] = PersonalTask.objects.filter(student=user).order_by('status', '-created_at')
        context['created_tasks'] = PersonalTask.objects.filter(teacher=user).order_by('-created_at')
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user

# Главная страница
def home(request):
    return render(request, "home.html")

# Страница "О нас"
def about(request):
    return render(request, "about.html")
