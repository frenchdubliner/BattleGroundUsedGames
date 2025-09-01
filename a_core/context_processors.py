from django.db.models import Sum, Avg, Count
from games.models import Game

def game_stats(request):
    """
    Context processor to provide game statistics to all templates
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Admin can see all games
            total_games = Game.objects.count()
            total_value = Game.objects.aggregate(total=Sum('price'))['total'] or 0
            avg_price = Game.objects.aggregate(avg=Avg('price'))['avg'] or 0
            active_sellers = Game.objects.values('user').distinct().count()
        else:
            # Regular users can only see their own games
            total_games = Game.objects.filter(user=request.user).count()
            total_value = Game.objects.filter(user=request.user).aggregate(total=Sum('price'))['total'] or 0
            avg_price = Game.objects.filter(user=request.user).aggregate(avg=Avg('price'))['avg'] or 0
            active_sellers = None
    else:
        # Anonymous users see no games
        total_games = 0
        total_value = 0
        avg_price = 0
        active_sellers = None
    
    return {
        'total_games': total_games,
        'total_value': total_value,
        'avg_price': round(avg_price, 2) if avg_price else 0,
        'active_sellers': active_sellers,
    }

