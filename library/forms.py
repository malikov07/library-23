from django import forms
from .models import Book

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title","description","image","serial_id")
        widgets = {
            'description': forms.TextInput(attrs={'required': False}),
        }