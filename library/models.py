from django.db import models
from students.models import Student


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    created_date = models.DateField(auto_now_add=True)


class Book(models.Model):
    serial_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=60)
    description = models.TextField(null=True,blank=True)
    publish_date = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to="library/books", blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Book_category(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)


class Author(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, null=True)
    birth_date = models.DateField(null=True)
    description = models.TextField(null=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Book_author(models.Model):
    book = models.ForeignKey(Book,related_name="authors" ,on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.book.name + ' -> ' + self.author.first_name


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
