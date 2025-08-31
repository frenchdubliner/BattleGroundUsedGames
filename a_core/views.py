from django.shortcuts import render

def help_support(request):
    """Display help and support contact information"""
    return render(request, 'help_support.html')
