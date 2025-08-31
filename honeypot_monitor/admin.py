from django.contrib import admin
from .models import HoneypotAttempt

@admin.register(HoneypotAttempt)
class HoneypotAttemptAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'username', 'is_login_attempt', 'timestamp', 'short_user_agent']
    list_filter = ['is_login_attempt', 'timestamp', 'ip_address']
    search_fields = ['ip_address', 'username', 'user_agent']
    readonly_fields = ['ip_address', 'user_agent', 'username', 'timestamp', 'is_login_attempt']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        """Prevent manual creation of honeypot attempts"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing of honeypot attempts"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion for cleanup"""
        return True
