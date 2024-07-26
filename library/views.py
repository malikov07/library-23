from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book,Book_author,Rental
from students.models import Student
from .forms import AddBookForm
from django.db.models import Q,Count
from django.utils import timezone
from django.urls import reverse
import json

# Create your views here.
class LibraryPageView(LoginRequiredMixin, View):
    def get(self,request):
        return render(request, "library/library.html")

class BooksListView(LoginRequiredMixin, View):
    def get(self,request):
        search = request.GET.get("search","")
        books = Book.objects.filter(
            title__icontains=search
        ) | Book.objects.filter(
            description__icontains=search
        ) | Book.objects.filter(
            serial_id__icontains=search
        )

        # Filter books by author first name
        author_books = Book.objects.filter(
            id__in=Book_author.objects.filter(
                author__first_name__icontains=search
            ).values_list('book_id', flat=True)
        )
        
        # Combine the querysets and remove duplicates
        books = (books | author_books).distinct()
        context = {
          "books": books,
          "search_value": search
        }
        return render(request, "library/books.html",context)
    
class AddBookView(LoginRequiredMixin, View):
    def get(self,request):
        scanned_result = request.GET["scanned_result"]
        student_id = request.GET.get("student_id","")
        return_date = request.GET.get("return_date","")
        class_id = request.GET.get("class_id","")
        context = {
            "scanned_result": scanned_result,
            "student_id": student_id,
            "return_date": return_date,
            "class_id": class_id,
        }
        return render(request, "library/addbook.html",context)
    
    def post(self,request):
        student_id = request.POST.get("student_id","")
        return_date = request.POST.get("return_date","")
        class_id = request.POST.get("class_id","")
        book_form = AddBookForm(request.POST,request.FILES)
        if book_form.is_valid():
            book = book_form.save(commit=False)  # Get the book instance without saving it to the database
            book.save()
            if student_id == "" and return_date == "":
                return redirect("books")
            else:
                student = Student.objects.get(id=student_id)
                rental = Rental.objects.create(
                    student=student,
                    book=book,
                    return_date=return_date
                )
                return redirect(f"{reverse('class', args=[class_id])}")
        else:
            scanned_result = request.GET["scanned_result"]

            context = {
                "returned_data": request.POST,
                "text": book_form.errors,
                "scanned_result": scanned_result
            }
            return render(request, "library/addbook.html",context) 
        
class UpdateBookView(LoginRequiredMixin, View):
    def get(self,request,id):
        book = Book.objects.get(id=id)
        context = {
            "returned_data": book,
            "update":True
        }
        return render(request, "library/addbook.html",context)
    
    def post(self,request,id):
        book = Book.objects.get(id=id)
        book_form = AddBookForm(request.POST,request.FILES,instance=book)
        if book_form.is_valid():
            book_form.save()
            return redirect("books")
        else:
            scanned_result = request.GET["scanned_result"]

            context = {
                "returned_data": request.POST,
                "text": book_form.errors,
                "scanned_result": scanned_result
            }
            return render(request, "library/addbook.html",context) 

# class DeleteBookView(View):
#     def get(self,request,id):
#         book = Book.objects.get(id=id)
#         context = {
#             "book_name": book.title
#         }
#         return render(request, "library/delete_confirm.html",context)
    
#     def post(self,request,id):
#         book = Book.objects.get(id=id)
#         book.delete()
#         return redirect("books")
         

class RentalListView(LoginRequiredMixin, View):
    def get(self,request):
        search = request.GET.get("search","")
        rentals = Rental.objects.filter(book__title__icontains = search) or Rental.objects.filter(student__first_name__icontains = search) or Rental.objects.filter(student__last_name__icontains = search)
        context = {
            "rentals":rentals,
            "search":search,
        }
        return render(request, "library/rentals.html", context)
    

class BooksAreReadedList(LoginRequiredMixin, View):
    def get(self,request):
        rentals = Rental.objects.filter(is_active=True)
        data={}
        for i in rentals:
            if i.book.title not in data:
                data[i.book.title]=rentals.filter(book__title = i.book.title).count()

        context = {
            'data': data,
        }
        return render(request, 'library/readingbooks.html', context)
    

class BooksShouldReturned(LoginRequiredMixin, View):
    def get(self,request):
        rentals = Rental.objects.filter(return_date__lte = timezone.now())
        context = {
            "old_rentals":rentals
        }
        return render(request,"library/requiredbooks.html",context)
    

class EndRentalView(LoginRequiredMixin, View):
    def post(self,request):
        rental_id = request.POST.get("rental_id")
        class_id = request.POST.get("class_id")
        rental = Rental.objects.get(id=rental_id)
        rental.is_active = False
        rental.save()
        class_detail_url = reverse('class', args=[class_id])
        return redirect(class_detail_url)