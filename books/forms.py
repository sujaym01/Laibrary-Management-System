# from django import forms
# from .models import BookCategory, Book, BorrowingHistory,Comment

# class CategoryForm(forms.ModelForm):
#     class Meta: 
#         model = BookCategory
#         fields = '__all__'

# class BooksForm(forms.ModelForm):
#     class Meta: 
#         model = Book
#         fields = '__all__'
#         # exclude = ['.....']
        
# class BorrowingHistoryForm(forms.ModelForm):
#     class Meta: 
#         model = BorrowingHistory
#         fields = '__all__'

# class CommentForm(forms.ModelForm):
#     class Meta: 
#         model = Comment
#         fields = ['name', 'comment_body']


from django import forms
from . import models

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['categories', 'title', 'description','image', 'price']

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['name', 'email', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            # If the comment instance has a user associated with it, prepopulate name and email
            # Assuming you have a user field in Comment model
            self.fields['name'].initial = self.instance.user.get_full_name()
            # self.fields['name'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            
        elif self.instance and not self.instance.user:
            # If the comment instance doesn't have a user, prepopulate with current user (if authenticated)
            user = self.initial.get('user')
            if user and user.is_authenticated:
                # self.fields['name'].initial = user.username
                self.fields['name'].initial = user.get_full_name()
                self.fields['email'].initial = user.email