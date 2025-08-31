from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from games.models import Game

def game_stats(request):
    """Context processor to provide game statistics for the sidebar"""
    context = {}
    
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Admin users see total games count
            context['total_games_count'] = Game.objects.count()
            context['user_games_count'] = Game.objects.filter(user=request.user).count()
        else:
            # Regular users see their own games count
            context['total_games_count'] = 0
            context['user_games_count'] = Game.objects.filter(user=request.user).count()
        
        # Active sellers (users who have created games) - only visible to admins
        if request.user.is_staff:
            context['active_sellers_count'] = Game.objects.values('user').distinct().count()
        else:
            context['active_sellers_count'] = None
        
        # Total sum of game prices - based on what user can see
        if request.user.is_staff:
            # Admin users see total value of all games
            total_sum = Game.objects.aggregate(total=Sum('price'))['total'] or 0
            context['total_games_sum'] = total_sum
        elif request.user.is_authenticated:
            # Regular users see total value of their own games
            total_sum = Game.objects.filter(user=request.user).aggregate(total=Sum('price'))['total'] or 0
            context['total_games_sum'] = total_sum
        else:
            # Unauthenticated users see no value
            context['total_games_sum'] = 0
        
        # Today's deals (games created today)
        today = timezone.now().date()
        context['today_deals_count'] = Game.objects.filter(
            created_at__date=today
        ).count()
    else:
        # Unauthenticated users see no stats
        context['total_games_count'] = 0
        context['user_games_count'] = 0
        context['active_sellers_count'] = 0
        context['today_deals_count'] = 0
    
    return context
