from django.contrib import admin

from books.models import Book, BookCopy, Category, Publisher

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(BookCopy)
