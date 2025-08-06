from django.contrib import admin
from .models import PublishOpportunity

@admin.register(PublishOpportunity)
class PublishOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'status', 'application_deadline', 'created_at')
    list_filter = ('status', 'type', 'application_deadline')
    search_fields = ('title', 'provider__user__username') 