from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from students.models import Sinf, Student
from library.models import Book,Rental
from .forms import StudentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from collections import defaultdict
import json


# Create your views here.
class ClassesView(LoginRequiredMixin, View):
    def get(self, request):
        classes = Sinf.objects.all()
        context = {"classes": classes}
        return render(request, "students/classes.html", context)


class ClassView(LoginRequiredMixin, View):
    def get(self, request, id):
        sinf = Sinf.objects.get(id=id)
        students = Student.objects.filter(sinf=sinf)
        students_with_books = []
        
        for student in students:
            rental = Rental.objects.filter(student=student)
            rental = rental.filter(status = 'r')
            students_with_books.append((student, list(rental)))

        context = {
            'students_with_books': students_with_books,
            "class_id":sinf.id,
            "sinf":sinf
        }
        return render(request, "students/class.html", context)


class ScanView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "students/scan.html")

    def post(self, request):
        data = json.loads(request.body)
        scanned_result = data.get("result")
        task = data.get("function")
        if task == "addbook":
            try:
                book = Book.objects.get(serial_id=scanned_result)
                book_info = {
                    "serial_id":book.serial_id,
                    "title": book.title,
                    "description": book.description,
                }
                response_data = {"success": True, "book_info": book_info}
            except Book.DoesNotExist:
                redirect_url = f"{reverse('addbook')}?scanned_result={scanned_result}"

                response_data = {"redirect": True, "redirect_url": redirect_url}
            return JsonResponse(response_data)
        
        elif task == "search_book_by_scan":
            try:
                book = Book.objects.get(serial_id=scanned_result)
                book_info = {
                    "serial_id":book.serial_id,
                    "title": book.title,
                    "description": book.description,
                }
                response_data = {"success": True, "book_info": book_info}
            except Book.DoesNotExist:
                response_data = {"bookDoesNotExist": True}
            return JsonResponse(response_data)
        
        elif task == "newrental":
            student_id = data.get("student_id")
            return_date = data.get("return_date")
            if return_date:
                try:
                    student = Student.objects.get(id=student_id)
                    book = Book.objects.get(serial_id=scanned_result)
                    new_rental = Rental.objects.create(
                        book=book,
                        student=student,
                        return_date=return_date
                    )
                    new_rental.save()
                    redirect_url = f"{reverse('class', args=[student.sinf.id])}"
                    response_data = {"rentalAdded": True, "redirect_url": redirect_url}
                    return JsonResponse(response_data)
                except Book.DoesNotExist:
                    student = Student.objects.get(id=student_id)
                    redirect_url = f"{reverse('addbook')}?scanned_result={scanned_result}&student_id={student_id}&return_date={return_date}&class_id={student.sinf.id}"
                    response_data = {"redirect": True, "redirect_url": redirect_url}
            else:
                response_data = {"noReturnDate": True}
            return JsonResponse(response_data)
        

class StudentListView(LoginRequiredMixin, View):
    def get(self,request):
        students = Student.objects.all()
        students_by_class = defaultdict(list)
        count = Student.objects.count()
        for student in students:
            students_by_class[student.sinf].append(student)
        
        context = {
        'students_by_class': dict(students_by_class),
        "count":count
    }
        return render(request, "students/students.html", context)
    

class AddStudent(LoginRequiredMixin, View):
    def get(self,request):
        class_id = request.GET["class_id"]
        context = {
            "class_id":class_id,
        }
        return render(request,"students/addstudent.html",context)

    def post(self,request):

        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.sinf = Sinf.objects.get(id=request.POST["class_id"])
            student.save()
            return redirect("students")
        else:
            return render(request, "students/addstudent.html", {
                "text": form.errors,
                "class_id": request.POST["class_id"],
            })


        # first_name = request.POST["first_name"]
        # last_name = request.POST["last_name"]
        # third_name = request.POST["third_name"]
        # birth_date = request.POST["birth_date"]
        # phone_number = request.POST["phone_number"]
        # address = request.POST["address"]
        # sinf = Sinf.objects.get(id = request.POST["class_id"])

        # new_student = Student.objects.create(
        #     first_name=first_name,
        #     last_name=last_name,
        #     third_name=third_name,
        #     birth_date=birth_date,
        #     phone_number=phone_number,
        #     address=address,
        #     sinf=sinf
        # )
        # new_student.save()
        # return redirect("students")

    

class UpdateStudent(LoginRequiredMixin, View):
    def get(self,request):
        student_id = request.GET["student_id"]
        student = Student.objects.get(id=student_id)
        context = {
            "student":student,
            "update":True,
        }
        return render(request,"students/addstudent.html",context)

    def post(self,request):
        student = Student.objects.get(id=request.POST["student_id"])

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        third_name = request.POST["third_name"]
        birth_date = request.POST.get("birth_date",None)
        phone_number = request.POST["phone_number"]
        address = request.POST["address"]
        

        
        student.first_name=first_name
        student.last_name=last_name
        student.third_name=third_name
        if birth_date:
            student.birth_date=birth_date
        student.phone_number=phone_number
        student.address=address
        student.save()
        return redirect("students")
    
class DeleteStudent(LoginRequiredMixin,View):
    def get(self,request,id):
        student = Student.objects.get(id = id)
        context = {
            "student":student
        }
        return render(request,"students/warning.html",context)

    def post(self,request,id):
        student = Student.objects.get(id = id)
        student.delete()
        return redirect("students")

    


from .forms import PhotoForm

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'students/upload.html', {'form': form})