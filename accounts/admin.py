from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TutorProfile, ProviderProfile

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

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = custom_fieldsets
    add_fieldsets = custom_add_fieldsets
    pass

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'course', 'year', 'cgpa')
    list_filter = ('course', 'year')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id')
    ordering = ('user__first_name',)

@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'designation', 'office_location')
    list_filter = ('department', 'designation')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    ordering = ('user__first_name',)

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_person', 'industry', 'company_size')
    list_filter = ('industry', 'company_size')
    search_fields = ('user__username', 'company_name', 'contact_person')
    ordering = ('company_name',)
