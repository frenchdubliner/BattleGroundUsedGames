from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from a_users.models import Profile
import csv

def is_admin_user(user):
    """Check if user is admin/staff"""
    return user.is_authenticated and user.is_staff

def help_support(request):
    """Display help and support contact information"""
    return render(request, 'help_support.html')

@user_passes_test(is_admin_user)
def admin_users_dashboard(request):
    """Admin-only view showing all users in a table format"""
    User = get_user_model()
    users = User.objects.all().select_related('profile').order_by('-date_joined')
    
    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
        
        writer = csv.writer(response)
        # Write header row
        writer.writerow([
            'User ID', 'Username', 'Email', 'First Name', 'Last Name', 'Phone Number', 
            'Drop Off Location', 'Payment Choice', 'Status', 'Is Staff', 'Date Joined'
        ])
        
        # Write data rows
        for user in users:
            writer.writerow([
                user.id,
                user.username,
                user.email or '',
                user.first_name or '',
                user.last_name or '',
                user.profile.phone_number if hasattr(user, 'profile') and user.profile.phone_number else '',
                user.profile.get_dropoff_location_display() if hasattr(user, 'profile') and user.profile.dropoff_location else 'Not Set',
                user.profile.get_payment_choice_display() if hasattr(user, 'profile') and user.profile.payment_choice else 'Not Set',
                'Active' if user.is_active else 'Inactive',
                'Yes' if user.is_staff else 'No',
                user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    # Handle user deletion
    if request.method == 'POST' and 'delete_user' in request.POST:
        user_id = request.POST.get('delete_user')
        try:
            user_to_delete = User.objects.get(id=user_id)
            if user_to_delete != request.user:  # Prevent admin from deleting themselves
                username = user_to_delete.username
                user_to_delete.delete()
                messages.success(request, f'User "{username}" has been deleted successfully.')
            else:
                messages.error(request, 'You cannot delete your own account.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        return redirect('admin_users_dashboard')
    
    context = {
        'users': users,
    }
    
    return render(request, 'admin_users_dashboard.html', context)
