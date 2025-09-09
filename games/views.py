from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from .models import Game
from .forms import GameForm, AdminGameForm
import csv
import os
import zipfile
import subprocess
from django.conf import settings
from django.template.loader import render_to_string

def is_admin_user(user):
    """Check if user is an admin/staff user"""
    return user.is_authenticated and user.is_staff

def game_list(request):
    """Display games - users see only their own games, admins see all games"""
    if request.user.is_authenticated and request.user.is_staff:
        # Admin users can see all games
        games = Game.objects.all().order_by('-created_at')
    elif request.user.is_authenticated:
        # Regular users can only see their own games
        games = Game.objects.filter(user=request.user).order_by('-created_at')
    else:
        # Unauthenticated users see no games
        games = Game.objects.none()
    
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def add_game(request):
    """Allow users to add a new game"""
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            messages.success(request, f'Game "{game.name}" added successfully!')
            return redirect('games:game_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GameForm()
    
    return render(request, 'games/add_game.html', {'form': form})

def game_detail(request, game_id):
    """Display detailed information about a specific game"""
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'games/game_detail.html', {'game': game})

@login_required
def my_games(request):
    """Display games owned by the current user"""
    games = Game.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'games/my_games.html', {'games': games})

@login_required
def edit_game(request, game_id):
    """Allow users to edit their own games, or admins to edit any game"""
    game = get_object_or_404(Game, id=game_id)
    
    # Check if the user owns this game OR is an admin
    if game.user != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit your own games.')
        return redirect('games:game_detail', game_id=game_id)
    
    # Use AdminGameForm for admins, GameForm for regular users
    if request.user.is_staff:
        form_class = AdminGameForm
    else:
        form_class = GameForm
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, f'Game "{game.name}" updated successfully!')
            return redirect('games:game_detail', game_id=game_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = form_class(instance=game)
    
    return render(request, 'games/edit_game.html', {'form': form, 'game': game})

@login_required
def delete_game(request, game_id):
    """Allow users to delete their own games"""
    game = get_object_or_404(Game, id=game_id)
    
    # Check if the user owns this game
    if game.user != request.user:
        messages.error(request, 'You can only delete your own games.')
        return redirect('games:game_detail', game_id=game_id)
    
    if request.method == 'POST':
        game_name = game.name
        game.delete()
        messages.success(request, f'Game "{game_name}" has been removed from the marketplace.')
        return redirect('games:game_list')
    
    # If it's a GET request, show confirmation page
    return render(request, 'games/delete_game_confirm.html', {'game': game})

@user_passes_test(is_admin_user)
def admin_only_games(request):
    """Admin-only view showing all games from all users in a table format"""
    games = Game.objects.all().select_related('user', 'user__profile').order_by('-created_at')
    
    # Get filter parameters
    game_id_filter = request.GET.get('game_id', '')
    condition_filter = request.GET.get('condition', '')
    printed_filter = request.GET.get('printed', '')
    user_filter = request.GET.get('user', '')
    drop_off_filter = request.GET.get('drop_off_location', '')
    
    # Apply filters
    if game_id_filter:
        games = games.filter(id=game_id_filter)
    if condition_filter:
        games = games.filter(condition=condition_filter)
    if printed_filter != '':
        games = games.filter(printed=printed_filter == 'true')
    if user_filter:
        games = games.filter(user__username__icontains=user_filter)
    if drop_off_filter:
        games = games.filter(user__profile__dropoff_location=drop_off_filter)
    
    # Handle CSV export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="games_export.csv"'
        
        writer = csv.writer(response)
        # Write header row
        writer.writerow([
            'Game ID', 'Game Name', 'Owner', 'Price', 'Condition', 'Missing Pieces', 
            'Missing Pieces Description', 'Smoking House', 'Musty Smell', 
            'Pet Exposure', 'Printed', 'Drop Off Location', 'Created Date'
        ])
        
        # Write data rows
        for game in games:
            writer.writerow([
                game.id,
                game.name,
                game.user.username,
                game.price,
                game.get_condition_display(),
                'Yes' if game.missing_pieces else 'No',
                game.description_of_missing_pieces or '',
                'Yes' if game.smoking_house else 'No',
                'Yes' if game.musty_smell else 'No',
                game.get_pet_display(),
                'Yes' if game.printed else 'No',
                game.user.profile.dropoff_location if hasattr(game.user, 'profile') else '',
                game.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    # Handle LaTeX export
    if request.GET.get('export') == 'latex':
        # Create exports directory if it doesn't exist
        exports_dir = settings.EXPORTS_ROOT
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)
        
        # Create a temporary directory for LaTeX files
        import tempfile
        import shutil
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Read the LaTeX template
            template_path = os.path.join(settings.BASE_DIR, 'games', 'templates', 'export_templates', 'tex_template.txt')
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Track successful PDF generations
            successful_pdfs = []
            failed_pdfs = []
            
            # Generate LaTeX files for each game and convert to PDF
            for game in games:
                # Create filename for this game
                safe_name = "".join(c for c in game.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_name = safe_name.replace(' ', '_')
                tex_filename = f"game_{game.id}_{safe_name}.tex"
                pdf_filename = f"game_{game.id}_{safe_name}.pdf"
                
                tex_filepath = os.path.join(temp_dir, tex_filename)
                pdf_filepath = os.path.join(exports_dir, pdf_filename)
                
                # Replace template placeholders with actual values
                game_content = template_content.replace('game.id', str(game.id))
                game_content = game_content.replace('game.condition', game.get_condition_display())
                game_content = game_content.replace('game.price', str(game.price))
                
                # Handle missing components
                if game.missing_pieces:
                    missing_components = f"Missing Components: {game.description_of_missing_pieces or 'Yes'}"
                else:
                    missing_components = "All Components Present"
                game_content = game_content.replace('missingcomponents', missing_components)
                
                # Handle smoking household
                if game.smoking_house:
                    smoking_household = "Smoking Household: Yes"
                else:
                    smoking_household = "Smoking Household: No"
                game_content = game_content.replace('smokinghousehold', smoking_household)
                
                # Handle animal condition
                if game.pet != 'none':
                    animal_condition = f"Animal Exposure: {game.get_pet_display()}"
                else:
                    animal_condition = "Animal Exposure: None"
                game_content = game_content.replace('animalcondition', animal_condition)
                
                # Handle musty smell
                if game.musty_smell:
                    musty_smell = "Musty Smell: Yes"
                else:
                    musty_smell = "Musty Smell: No"
                game_content = game_content.replace('mustysmell', musty_smell)
                
                # Write the LaTeX file
                with open(tex_filepath, 'w', encoding='utf-8') as f:
                    f.write(game_content)
                
                # Convert LaTeX to PDF using pdflatex
                try:
                    # Run pdflatex command
                    result = subprocess.call([
                        '/usr/bin/pdflatex',  # Use absolute path
                        # 'pdflatex',
                        '-interaction=nonstopmode',
                        '-output-directory=' + temp_dir,
                        tex_filepath
                    ], cwd=temp_dir)
                    
                    # Check if PDF was generated successfully
                    generated_pdf = os.path.join(temp_dir, pdf_filename)
                    if result == 0 and os.path.exists(generated_pdf):
                        # Move PDF to exports directory
                        shutil.move(generated_pdf, pdf_filepath)
                        successful_pdfs.append(pdf_filename)
                        
                        # Update the game's printed field to True since PDF was generated
                        game.printed = True
                        game.save()
                    else:
                        failed_pdfs.append(f"{game.name} (LaTeX compilation failed)")
                        
                except Exception as e:
                    failed_pdfs.append(f"{game.name} (Error: {str(e)})")
            
            # Clean up temporary LaTeX files and auxiliary files
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(('.tex', '.aux', '.log', '.out')):
                        try:
                            os.remove(os.path.join(root, file))
                        except:
                            pass
            
            # Show success/error messages
            if successful_pdfs:
                messages.success(request, f'Successfully generated {len(successful_pdfs)} PDF files in the exports folder. The "printed" field has been set to True for these games.')
            if failed_pdfs:
                messages.error(request, f'Failed to generate PDFs for: {", ".join(failed_pdfs)}')
            
            # Redirect back to the admin dashboard
            return redirect('games:admin_only_games')
            
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
    
    # Handle PDF merge
    if request.GET.get('export') == 'merge':
        exports_dir = settings.EXPORTS_ROOT
        
        if not os.path.exists(exports_dir):
            messages.error(request, 'No exports folder found. Please generate PDFs first.')
            return redirect('games:admin_only_games')
        
        # Get all PDF files in the exports directory
        pdf_files = [f for f in os.listdir(exports_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            messages.error(request, 'No PDF files found in the exports folder. Please generate PDFs first.')
            return redirect('games:admin_only_games')
        
        # Sort PDF files by name for consistent ordering
        pdf_files.sort()
        
        # Create input file list for pdftk
        input_files = []
        for pdf_file in pdf_files:
            input_files.append(os.path.join(exports_dir, pdf_file))
        
        # Create merged PDF filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        merged_filename = f"merged_games_{timestamp}.pdf"
        merged_filepath = os.path.join(exports_dir, merged_filename)
        
        try:
            # Use pdftk to merge PDFs
            # pdftk input1.pdf input2.pdf ... cat output merged.pdf
            cmd = ['/usr/bin/pdftk'] + input_files + ['cat', 'output', merged_filepath]
            
            result = subprocess.call(cmd)
            
            if result == 0 and os.path.exists(merged_filepath):
                # Read the merged PDF and return it as download
                with open(merged_filepath, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{merged_filename}"'
                
                # Delete all individual PDF files after successful download
                for pdf_file in pdf_files:
                    try:
                        os.remove(os.path.join(exports_dir, pdf_file))
                    except:
                        pass
                
                # Delete the merged PDF file as well
                try:
                    os.remove(merged_filepath)
                except:
                    pass
                
                return response
            else:
                messages.error(request, 'Failed to merge PDFs. Please check if pdftk is installed.')
                return redirect('games:admin_only_games')
                
        except Exception as e:
            messages.error(request, f'Error merging PDFs: {str(e)}')
            return redirect('games:admin_only_games')
    
    # Get unique values for filter dropdowns
    conditions = Game.CONDITION_CHOICES
    users = Game.objects.values_list('user__username', flat=True).distinct().order_by('user__username')
    
    # Get drop off location choices from Profile model (not from Game model)
    from a_users.models import Profile
    drop_off_locations = Profile.DROPOFF_LOCATION_CHOICES
    
    context = {
        'games': games,
        'conditions': conditions,
        'users': users,
        'drop_off_locations': drop_off_locations,
        'current_filters': {
            'game_id': game_id_filter,
            'condition': condition_filter,
            'printed': printed_filter,
            'user': user_filter,
            'drop_off_location': drop_off_filter,
        }
    }
    
    return render(request, 'games/admin_only_games.html', context)
