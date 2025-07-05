from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, TutorProfile, ProviderProfile

<<<<<<< HEAD
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Placement Management', {
            'fields': ('user_type', 'phone', 'is_verified')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Placement Management', {
            'fields': ('user_type', 'phone', 'is_verified')
        }),
    )

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
=======
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(TutorProfile)
admin.site.register(ProviderProfile)
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
