from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from allauth.account.models import EmailAddress
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('account_login')
    return render(request, 'a_users/profile.html', {'profile': profile})

def profile_edit_view(request):
    # Check if admin is editing another user's profile
    user_id = request.GET.get('user_id')
    is_admin_editing = False
    target_user = request.user
    
    if user_id and request.user.is_staff:
        try:
            target_user = User.objects.get(id=user_id)
            is_admin_editing = True
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('profile')
    
    form = ProfileForm(instance=target_user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=target_user.profile)
        if form.is_valid():
            form.save()
            if is_admin_editing:
                messages.success(request, f'Profile for {target_user.username} updated successfully')
                return redirect('admin_users_dashboard')
            else:
                messages.success(request, 'Profile updated successfully')
                return redirect('profile')

    if request.path == reverse('profile_onboarding'):
        onboarding = True
    else:
        onboarding = False

    return render(request, 'a_users/profile_edit.html', {
        'form': form, 
        'onboarding': onboarding, 
        'is_admin_editing': is_admin_editing,
        'target_user': target_user
    })

@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')

@login_required
def profile_emailchange(request):

    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():

            #check if email is already in use
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use')
                return redirect('profile_settings')

            # Save the new email
            old_email = request.user.email
            form.save()
            
            # Handle email confirmation for the new email
            if email != old_email:
                try:
                    # Create or get the email address object
                    email_address, created = EmailAddress.objects.get_or_create(
                        user=request.user,
                        email=email,
                        defaults={'primary': True}
                    )
                    
                    # Send confirmation email
                    current_site = get_current_site(request)
                    email_address.send_confirmation(request, signup=False)
                    
                    messages.success(request, f'Email changed to {email}. Please check your email to confirm the new address.')
                except Exception as e:
                    messages.warning(request, f'Email changed but confirmation email could not be sent: {str(e)}')
            else:
                messages.success(request, 'Email updated successfully')

            return redirect('profile_settings')
        else:
            # Debug: show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('profile_settings')
            

    return redirect('home')

@login_required
def profile_emailverify(request):
    try:
        # Get the user's primary email address
        email_address = EmailAddress.objects.filter(user=request.user, primary=True).first()
        
        if email_address:
            if email_address.verified:
                messages.info(request, 'Your email is already verified.')
            else:
                # Send confirmation email
                email_address.send_confirmation(request, signup=False)
                messages.success(request, 'Verification email sent! Please check your email to verify your address.')
        else:
            messages.warning(request, 'No email address found to verify.')
            
    except Exception as e:
        messages.error(request, f'Could not send verification email: {str(e)}')
    
    return redirect('profile_settings')

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted successfully')
        return redirect('home')
        
    return render(request, 'a_users/profile_delete.html')
