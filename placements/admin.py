from django.contrib import admin
from .models import PlacementRequest, PlacementReport, Message, VisitSchedule

@admin.register(PlacementRequest)
class PlacementRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'tutor', 'company_name', 'job_title', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'start_date', 'end_date', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'company_name', 'job_title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'provider_approved_at', 'tutor_approved_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'provider', 'tutor', 'company_name', 'job_title', 'job_description')
        }),
        ('Placement Details', {
            'fields': ('start_date', 'end_date', 'location', 'latitude', 'longitude')
        }),
        ('Status & Approval', {
            'fields': ('status', 'approved_by_tutor', 'provider_approved_at', 'tutor_approved_at')
        }),
        ('Documents', {
            'fields': ('documents',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PlacementReport)
class PlacementReportAdmin(admin.ModelAdmin):
    list_display = ('placement_request', 'submitted_at', 'report_file')
    list_filter = ('submitted_at',)
    search_fields = ('placement_request__student__user__first_name', 'placement_request__student__user__last_name')
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'sender__user_type', 'recipient__user_type')
    search_fields = ('sender__username', 'recipient__username', 'subject', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ('placement_request', 'tutor', 'visit_date', 'purpose', 'completed')
    list_filter = ('completed', 'visit_date', 'tutor__user_type')
    search_fields = ('placement_request__company_name', 'tutor__username', 'purpose')
    ordering = ('visit_date',)
    readonly_fields = ('created_at',)
