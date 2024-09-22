from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book,Rental,Score
from students.models import Student,Sinf
from .forms import AddBookForm
from django.db.models import Q,Count,Sum
from django.utils import timezone
from django.urls import reverse
from django.db.models.functions import TruncMonth
import base64
from django.core.files.base import ContentFile
import random
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

        
        context = {
          "books": books,
          "search_value": search
        }
        return render(request, "library/books.html",context)
    
class AddBookView(LoginRequiredMixin, View):
    def get(self, request):
        scanned_result = request.GET.get("scanned_result", "")
        student_id = request.GET.get("student_id", "")
        return_date = request.GET.get("return_date", "")
        class_id = request.GET.get("class_id", "")
        context = {
            "scanned_result": scanned_result,
            "student_id": student_id,
            "return_date": return_date,
            "class_id": class_id,
        }
        return render(request, "library/addbook.html", context)

    def post(self, request):
        student_id = request.POST.get("student_id", "")
        return_date = request.POST.get("return_date", "")
        class_id = request.POST.get("class_id", "")
        
        # Check if a photo was taken with the camera
        photo_data = request.POST.get("photo_data", "")
        image_file = request.FILES.get("image")  # File input from form
        
        # Create form instance with POST data and FILES
        book_form = AddBookForm(request.POST, request.FILES)
        
        # If form is valid
        if book_form.is_valid():
            book = book_form.save(commit=False)  
            if photo_data:
                format, imgstr = photo_data.split(';base64,')
                ext = format.split('/')[-1]  
                image_data = ContentFile(base64.b64decode(imgstr), name=f'book_image.{ext}')
                book.image = image_data  
            elif image_file:
                book.image = image_file

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
            # If form is not valid, re-render the form with error messages
            scanned_result = request.GET.get("scanned_result", "")
            context = {
                "returned_data": request.POST,
                "text": book_form.errors,
                "scanned_result": scanned_result
            }
            return render(request, "library/addbook.html", context) 
        
class UpdateBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        context = {
            "returned_data": book,
            "update": True
        }
        return render(request, "library/addbook.html", context)
    
    def post(self, request, id):
        book = get_object_or_404(Book, id=id)
        photo_data = request.POST.get("photo_data", "")
        book_form = AddBookForm(request.POST, request.FILES, instance=book)

        if book_form.is_valid():
            # If base64 photo data exists, handle it
            if photo_data:
                format, imgstr = photo_data.split(';base64,')
                ext = format.split('/')[-1]
                image_data = ContentFile(base64.b64decode(imgstr), name=f'book_image.{ext}')
                book.image = image_data

            # Save the book with any new image data
            book_form.save()
            return redirect("books")
        else:
            # Handle `scanned_result` in the context if needed
            scanned_result = request.POST.get("scanned_result", "")

            context = {
                "returned_data": book,  # Ensure we pass the book instance to retain existing data
                "text": book_form.errors,
                "scanned_result": scanned_result,
                "update": True
            }
            return render(request, "library/addbook.html", context)

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
        rentals = Rental.objects.filter(status='r')
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
        rental.student.ball+=Score
        rental.student.save()
        rental.status = 'c'
        rental.save()
        class_detail_url = reverse('class', args=[class_id])
        return redirect(class_detail_url)
    

class CompleteRentalView(LoginRequiredMixin, View):
    def post(self,request):
        rental_id = request.POST.get("rental_id")
        rental = Rental.objects.get(id=rental_id)
        rental.status = 'c'
        rental.student.ball+=Score
        rental.student.save()
        rental.save()
        return redirect("rentals")
    

class CancelRental(LoginRequiredMixin,View):
    def post(self,request):
        rental = Rental.objects.get(id = request.POST["rental_id"])
        rental.status = 'd'
        rental.save()
        return redirect('rentals')
    

def generate_random_color():
    f = random.randint(0, 255)
    s = random.randint(0, 255)
    t = random.randint(0, 255)
    return f"rgba({f}, {s}, {t}, 0.6)",f"rgba({f}, {s}, {t}, 0.9)"


class StatisticsView(LoginRequiredMixin, View):
    def get(self,request):
        rentals_by_month= Rental.objects.filter(status='c') 
        rentals_by_month=rentals_by_month.annotate(month=TruncMonth('last_update'))
        rentals_by_month=rentals_by_month.values('month')
        rentals_by_month=rentals_by_month.annotate(total=Count('id'))
        rentals_by_month=rentals_by_month.order_by('month')

        number_of_students = Student.objects.all().count()
        reading_students = Student.objects.filter(id__in = Rental.objects.filter(status='r').values('student')).count()
        r_percent = round(reading_students*100/number_of_students, 2)
        nr_percent = 100-r_percent
        sinf_ball_sum = Sinf.objects.annotate(total_ball=Sum('student__ball')).order_by('number','letter')
        
        classes_rank = Sinf.objects.annotate(total_ball=Sum('student__ball')).order_by('-total_ball')

        colors = [generate_random_color() for _ in sinf_ball_sum]

        top_students = Student.objects.order_by('-ball')[:5]

        context = {
            'rentals_by_month': rentals_by_month,
            'r_percent':r_percent,
            'nr_percent':nr_percent,
            'sinf_ball_sum':sinf_ball_sum,
            'colors':colors,
            'top_students':top_students,
            'classes_rank':classes_rank,

        }
        return render(request, "library/statistics/chart.html",context)