from django.db import models

# Create your models here.
class LetterChoices(models.TextChoices):
    A = ("a","A")
    B = ("b","B")
    V = ("v","V")
    D = ("d","D")

class Sinf(models.Model):
    number = models.IntegerField()
    letter = models.CharField(max_length=1, null=True, blank=True, choices=LetterChoices.choices)

    def __str__(self):
        if self.letter:
            return f"{self.number}{self.letter}".upper()
        return f"{self.number}"
    
    class Meta:
        ordering = ["number","letter"]


class Student(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    third_name = models.CharField(max_length=60, null=True)
    birth_date = models.DateField(null=True)
    sinf = models.ForeignKey(Sinf, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.first_name + self.last_name

    class Meta:
        ordering = ["sinf", "first_name","last_name"]