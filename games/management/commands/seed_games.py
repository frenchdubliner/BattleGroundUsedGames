from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from games.models import Game
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with fake game data'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, default=10, help='Number of games to create')

    def handle(self, *args, **options):
        number = options['number']
        
        # Get all users (we need at least one user to assign games to)
        users = list(User.objects.all())
        
        if not users:
            self.stdout.write(
                self.style.ERROR('No users found. Please create at least one user first.')
            )
            return
        
        # Game names for variety
        game_names = [
            "Settlers of Catan", "Ticket to Ride", "Pandemic", "Carcassonne", 
            "Dominion", "7 Wonders", "Agricola", "Puerto Rico", "Power Grid",
            "Race for the Galaxy", "Stone Age", "Lords of Waterdeep", "Splendor",
            "King of Tokyo", "Love Letter", "The Resistance", "Codenames",
            "Azul", "Wingspan", "Root", "Gloomhaven", "Spirit Island"
        ]
        
        # Condition choices
        conditions = [
            ('new in shrink', 'New in Shrink- Original shrinkwrap/seal is intact. Never Opened'),
            ('like new', 'Like New- Pieces unpunched, cards wrapped, never played'),
            ('very good', 'Very Good- Pieces punched, Sorted. Rarely or never played. No discernible wear'),
            ('good', 'Good- Played but well maintained. Pieces unsorted. Box/book(s) shows signs of use'),
            ('fair', 'Fair- Discernible wear. Box/book(s) shows minor damage and/or have been slightly marked'),
            ('Poor', 'Poor- Worn but playable. Box/book(s) shows damage and/or have been significantly marked')
        ]
        
        # Pet choices
        pet_choices = [
            ('none', 'None'),
            ('cat', 'Cat'),
            ('dog', 'Dog')
        ]
        
        games_created = 0
        
        for i in range(number):
            # Random user
            user = random.choice(users)
            
            # Random game name
            name = random.choice(game_names)
            
            # Random price between $10 and $100
            price = round(random.uniform(10.0, 100.0), 2)
            
            # Random condition
            condition, _ = random.choice(conditions)
            
            # Random boolean values
            missing_pieces = random.choice([True, False])
            smoking_house = random.choice([True, False])
            musty_smell = random.choice([True, False])
            
            # Random pet choice
            pet, _ = random.choice(pet_choices)
            
            # Description for missing pieces (if applicable)
            description_of_missing_pieces = ""
            if missing_pieces:
                descriptions = [
                    "Missing 2 cards", "Missing 1 dice", "Missing rulebook",
                    "Missing 3 pieces", "Missing scoring pad", "Missing player tokens"
                ]
                description_of_missing_pieces = random.choice(descriptions)
            
            # Create the game
            game = Game.objects.create(
                user=user,
                name=name,
                price=price,
                condition=condition,
                missing_pieces=missing_pieces,
                description_of_missing_pieces=description_of_missing_pieces,
                smoking_house=smoking_house,
                musty_smell=musty_smell,
                pet=pet,
                printed=False
            )
            
            games_created += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Created game: {game.name} - ${game.price} - {game.condition}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {games_created} games!')
        )
