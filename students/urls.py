from django.urls import path
from .views import ClassesView,ClassView,ScanView,StudentListView,photo_upload,AddStudent,UpdateStudent,DeleteStudent

urlpatterns = [
    path("",ClassesView.as_view(), name="classes"),
    path("<int:id>/",ClassView.as_view(), name="class"),
    path("scan/",ScanView.as_view(), name="scan"),
    path("students/",StudentListView.as_view(), name="students"),
    path('upload/', photo_upload, name='upload'),
    path('addstudent/', AddStudent.as_view(), name='addstudent'),
    path('updatestudent/', UpdateStudent.as_view(), name='updatestudent'),
    path('deletestudent/<int:id>/', DeleteStudent.as_view(), name='deletestudent'),
]
