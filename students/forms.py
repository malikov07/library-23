from django import forms
from .models import Photo
from .models import Student, Sinf

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'third_name', 'birth_date', 'sinf', 'phone_number', 'address']