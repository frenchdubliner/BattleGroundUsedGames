from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
import logging
from .models import HoneypotAttempt

# Set up logging for honeypot attempts
logger = logging.getLogger(__name__)

def honeypot_admin(request):
    """
    Honeypot admin view to trap bots and malicious users
    """
    # Log the attempt
    ip = request.META.get('REMOTE_ADDR', 'Unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    if request.method == 'POST':
        # Log login attempts
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        logger.warning(f'Honeypot login attempt - IP: {ip}, User-Agent: {user_agent}, Username: {username}')
        
        # Save to database
        HoneypotAttempt.objects.create(
            ip_address=ip,
            user_agent=user_agent,
            username=username,
            is_login_attempt=True
        )
        
        # Always show the same error message
        return render(request, 'honeypot/admin_login.html', {
            'title': 'Django administration',
            'site_title': 'Django administration',
            'site_header': 'Django administration',
            'error_message': 'Please enter the correct username and password for a staff account.',
        })
    
    # Log page access
    logger.warning(f'Honeypot accessed by IP: {ip}, User-Agent: {user_agent}')
    
    # Save to database
    HoneypotAttempt.objects.create(
        ip_address=ip,
        user_agent=user_agent,
        is_login_attempt=False
    )
    
    # Return a fake admin login page
    return render(request, 'honeypot/admin_login.html', {
        'title': 'Django administration',
        'site_title': 'Django administration',
        'site_header': 'Django administration',
    })
