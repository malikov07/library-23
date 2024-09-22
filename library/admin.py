from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book, Rental

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    list_display = ('id', 'serial_id', 'title', 'description', 'created_date', 'last_update')
    list_filter = ('created_date',)
    search_fields = ('title', 'description')
    list_display_links = ('id', 'serial_id', 'title')  # Make id, serial_id, and title clickable

@admin.register(Rental)
class RentalAdmin(ImportExportModelAdmin):
    list_display = ('id', 'book', 'student', 'created_date', 'return_date', 'status')
    list_filter = ('created_date', 'return_date', 'status')
    search_fields = ('book__title', 'student__first_name', 'student__last_name')
    list_display_links = ('id', 'book', 'student')  # Make id, book, and student clickable
