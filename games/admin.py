from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'price', 'condition', 'missing_pieces', 'printed', 'created_at']
    list_filter = ['condition', 'missing_pieces', 'smoking_house', 'musty_smell', 'pet', 'printed', 'created_at']
    search_fields = ['name', 'user__username', 'description_of_missing_pieces']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'user', 'price', 'condition')
        }),
        ('Game Condition', {
            'fields': ('missing_pieces', 'description_of_missing_pieces')
        }),
        ('Environmental Factors', {
            'fields': ('smoking_house', 'musty_smell', 'pet')
        }),
        ('Admin Only', {
            'fields': ('printed',),
            'classes': ('collapse',),
            'description': 'This information is only visible to admin users'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
