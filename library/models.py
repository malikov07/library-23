from django.db import models
from students.models import Student





class Book(models.Model):
    serial_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=60)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="library/books", blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-last_update","created_date"]


class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    created_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.book.title + ' -> ' + self.student.first_name
    
    class Meta:
        ordering = ["-created_date"]
