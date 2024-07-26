from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Book, Book_category, Author, Book_author, Rental

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'description', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('name', 'description')
    list_display_links = ('id', 'name')  # Make id and name clickable

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    list_display = ('id', 'serial_id', 'title', 'description', 'publish_date', 'created_date', 'last_update')
    list_filter = ('publish_date', 'created_date')
    search_fields = ('title', 'description')
    list_display_links = ('id', 'serial_id', 'title')  # Make id, serial_id, and title clickable

@admin.register(Book_category)
class BookCategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'book')
    list_filter = ('book',)
    search_fields = ('book__title',)
    list_display_links = ('id', 'book')  # Make id and book clickable

@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birth_date', 'description', 'last_update')
    list_filter = ('birth_date', 'last_update')
    search_fields = ('first_name', 'last_name', 'description')
    list_display_links = ('id', 'first_name', 'last_name')  # Make id, first name, and last name clickable

@admin.register(Book_author)
class BookAuthorAdmin(ImportExportModelAdmin):
    list_display = ('id', 'book', 'author')
    list_filter = ('book', 'author')
    search_fields = ('book__title', 'author__first_name', 'author__last_name')
    list_display_links = ('id', 'book', 'author')  # Make id, book, and author clickable

@admin.register(Rental)
class RentalAdmin(ImportExportModelAdmin):
    list_display = ('id', 'book', 'student', 'created_date', 'return_date', 'is_active')
    list_filter = ('created_date', 'return_date', 'is_active')
    search_fields = ('book__title', 'student__first_name', 'student__last_name')
    list_display_links = ('id', 'book', 'student')  # Make id, book, and student clickable
