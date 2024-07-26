from django.urls import path
from .views import ClassesView,ClassView,ScanView,StudentListView

urlpatterns = [
    path("",ClassesView.as_view(), name="classes"),
    path("<int:id>/",ClassView.as_view(), name="class"),
    path("scan/",ScanView.as_view(), name="scan"),
    path("students/",StudentListView.as_view(), name="students"),
]
