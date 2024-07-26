from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Sinf, Student

# Register the models with import-export functionality
@admin.register(Sinf)
class SinfAdmin(ImportExportModelAdmin):
    list_display = ('id','number', 'letter')
    list_filter = ('id','number', 'letter')
    search_fields = ('id','number', 'letter')
    list_display_links = ('id','number', 'letter')  # Make number and letter clickable

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('id','first_name', 'last_name', 'third_name', 'birth_date', 'sinf', 'phone_number', 'address')
    list_filter = ('id','sinf', 'birth_date')
    search_fields = ('id','first_name', 'last_name', 'third_name', 'sinf__number', 'sinf__letter')
    list_display_links = ('id','first_name', 'last_name', 'sinf')  # Make first name, last name, and sinf clickable
