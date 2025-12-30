from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Section, Material, ContentBlock, Test, CodingProblem, ShopItem, Achievement, Clan

# --- User Admin ---
admin.site.register(User, UserAdmin)

# --- Content Structure Admins ---

class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    extra = 0
    sortable_field_name = "order"

class CodingProblemInline(admin.StackedInline):
    model = CodingProblem
    extra = 0

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_filter = ('section__course', 'section')
    inlines = [ContentBlockInline, CodingProblemInline]
    search_fields = ('title', 'section__title')

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 0
    fields = ('title', 'order', 'xp_reward')
    show_change_link = True # Allows jumping to the full Material edit page to add blocks

class TestInline(admin.StackedInline):
    model = Test
    extra = 0

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [MaterialInline, TestInline]
    search_fields = ('title', 'course__title')

class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    fields = ('title', 'order')
    show_change_link = True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    inlines = [SectionInline]

# --- Other Models ---
admin.site.register(ShopItem)
admin.site.register(Achievement)
admin.site.register(Clan)
admin.site.register(ContentBlock) # Registered separately if needed
