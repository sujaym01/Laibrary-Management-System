# from django.shortcuts import render
# from books.models import Book,BookCategory

# def home(request, category_slug = None):
#     data = Book.objects.all()
#     if category_slug is not None:
#         category = BookCategory.objects.get(slug = category_slug)
#         data = Book.objects.filter(category  = category)
#     categories = BookCategory.objects.all()
#     return render(request, 'home.html', {'data' : data, 'category' : categories})

