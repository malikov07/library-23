from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from students.models import Sinf, Student
from library.models import Book,Rental
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
            rental = rental.filter(is_active = True)
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
                    "publish_date": book.publish_date.strftime('%d-%m-%Y')
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
                    "publish_date": book.publish_date.strftime('%d-%m-%Y')
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
        print(students_by_class)
        context = {
        'students_by_class': dict(students_by_class),
        "count":count
    }
        return render(request, "students/students.html", context)