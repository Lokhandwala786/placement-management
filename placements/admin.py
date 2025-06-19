from django.contrib import admin
from .models import PlacementRequest, PlacementReport, Message, VisitSchedule

@admin.register(PlacementRequest)
class PlacementRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'company_name', 'job_title', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'created_at')
    search_fields = ('company_name', 'job_title', 'student__user__username')

@admin.register(PlacementReport)
class PlacementReportAdmin(admin.ModelAdmin):
    list_display = ('placement_request', 'submitted_at')
    list_filter = ('submitted_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')

@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ('placement_request', 'tutor', 'visit_date', 'completed')
    list_filter = ('completed', 'visit_date')
