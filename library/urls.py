from django.urls import path
from .views import LibraryPageView,BooksListView,AddBookView,RentalListView,BooksAreReadedList,BooksShouldReturned,EndRentalView,UpdateBookView,CancelRental,CompleteRentalView,StatisticsView

urlpatterns = [
    path("",LibraryPageView.as_view(),name="library"),
    path("books/",BooksListView.as_view(),name="books"),
    path("add-book/",AddBookView.as_view(),name="addbook"),
    path("rentals/",RentalListView.as_view(),name="rentals"),
    path("books-are-being-readed/",BooksAreReadedList.as_view(),name="readingbooks"),
    path("required-books/",BooksShouldReturned.as_view(),name="requiredbooks"),
    path("endrental/",EndRentalView.as_view(),name="endrental"),
    path("update-book/<int:id>/",UpdateBookView.as_view(),name="update_book"),
    path("cancel-rental/",CancelRental.as_view(),name="cancel_rental"),
    path("complete-rental/",CompleteRentalView.as_view(),name="complete_rental"),
    path("statistics/",StatisticsView.as_view(),name="statistics"),
    
]