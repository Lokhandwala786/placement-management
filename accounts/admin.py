from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TutorProfile, ProviderProfile, Course, Department

# Helper for fieldsets
if UserAdmin.fieldsets:
    custom_fieldsets = UserAdmin.fieldsets + (
        ('Placement Management', {
            'fields': ('user_type', 'phone', 'is_verified')
        }),
    )
else:
    custom_fieldsets = (
        ('Placement Management', {
            'fields': ('user_type', 'phone', 'is_verified')
        }),
    )

base_add_fieldsets = getattr(UserAdmin, 'add_fieldsets', None)
if base_add_fieldsets:
    custom_add_fieldsets = base_add_fieldsets + (
        ('Placement Management', {
            'fields': ('user_type', 'phone', 'is_verified')
        }),
    )
else:
    custom_add_fieldsets = (
        ('Placement Management', {
            'fields': ('user_type', 'phone', 'is_verified')
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'duration_years', 'is_active', 'created_at']
    list_filter = ['is_active', 'duration_years']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_verified']
    list_filter = ['user_type', 'is_active', 'is_verified', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('user_type', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'phone'),
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'course', 'year', 'cgpa', 'tutor']
    list_filter = ['course', 'year', 'tutor']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'student_id']
    ordering = ['user__first_name']

@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'designation', 'office_location']
    list_filter = ['department', 'designation']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']
    ordering = ['user__first_name']

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'contact_person', 'industry']
    list_filter = ['industry']
    search_fields = ['company_name', 'contact_person', 'user__username']
    ordering = ['company_name']
