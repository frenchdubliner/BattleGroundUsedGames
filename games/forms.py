from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    """Form for regular users to add/edit games (excludes printed field)"""
    class Meta:
        model = Game
        fields = ['name', 'price', 'condition', 'missing_pieces', 'description_of_missing_pieces', 'smoking_house', 'musty_smell', 'pet']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'step': '0.01', 'min': '0.01'}),
            'condition': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'description_of_missing_pieces': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'rows': 3}),
            'smoking_house': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500'}),
            'musty_smell': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500'}),
            'pet': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
        }

class AdminGameForm(forms.ModelForm):
    """Form for admin users to edit games (includes printed and received fields)"""
    class Meta:
        model = Game
        fields = ['name', 'price', 'condition', 'missing_pieces', 'description_of_missing_pieces', 'smoking_house', 'musty_smell', 'pet', 'printed', 'received']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'step': '0.01', 'min': '0.01'}),
            'condition': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'description_of_missing_pieces': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'rows': 3}),
            'smoking_house': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500'}),
            'musty_smell': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500'}),
            'pet': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'printed': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500'}),
            'received': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500'}),
        }



