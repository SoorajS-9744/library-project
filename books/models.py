from django.db import models

class Book(models.Model):
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pub_date = models.DateField()
    rate = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return self.book_name