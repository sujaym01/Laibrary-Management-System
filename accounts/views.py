from django.shortcuts import render, redirect
from django.views.generic import FormView
from . forms import UserRegistrationForm, UserUpdateForm
from django.views.generic import RedirectView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from books.models import Book
from transactions.models import Transaction
from transactions.constants import BORROWED, RETURN
# Create your views here.


def send_password_change_email(user, subject, template):
    message = render_to_string(template, {
        'user': user,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class UserRegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        print(form.cleaned_data)
        login(self.request, user)
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     print(form.errors)
    #     print(form.cleaned_data)
    #     return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')
        # return reverse_lazy('home')

    
class UserLogoutView(RedirectView):
    url = reverse_lazy('home')  # Redirect to home after logout

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get(request, *args, **kwargs)

# class UserLogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('home')

class UserProfileUpdateView(LoginRequiredMixin,View):
    template_name = 'accounts/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('update_profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})

# class UserProfileUpdateView(LoginRequiredMixin,View):
#     template_name = 'accounts/update_profile.html'

#     def get(self, request):
#         form = UserUpdateForm(instance=request.user)
#         # return render(request, 'accounts/profile.html', {'form': form})
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = UserUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 self.request, 'Your profile has been updated successfully!!!')
#             return redirect('update_profile')
#         else:
#             print(form.errors)
#         return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        borrowed_books = Book.objects.filter(borrowers=request.user)
        # for book in borrowed_books:
        #     print(book.title, book.price, book.categories)

        # all_transactions = Transaction.objects.filter(account=request.user.account).order_by('-timestamp')
        # for transaction in all_transactions:
        #     print(transaction.amount, transaction.balance_after_transaction,transaction.transaction_type)

        # Create a list to store book details along with their borrowing history
        borrowed_books_details = []

        for book in borrowed_books:
            # Get the borrowing history for each book
            details = Transaction.objects.filter(
                account=request.user.account, 
                amount=book.price,
            ).order_by('-timestamp')

            # Add book and its history to the list
            borrowed_books_details.append({'book': book, 'details': details})

            # Extract transaction details for each book
            # transactions_for_book = [{'amount': transaction.amount, 'balance_after_transaction': transaction.balance_after_transaction}
            #                 for transaction in borrowed_books_details]
            
        context = {
            'user': request.user,
            # 'borrowed_books': borrowed_books,
            'borrowed_books_details': borrowed_books_details,
            # 'all_transactions': all_transactions,
        }
        return render(request, self.template_name, context=context)

@login_required
def password_change(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, 'Your password was successfully updated!')
                
                send_password_change_email(
                    request.user, 
                    'Password Changed',
                    'accounts/password_change_mail.html'
                    )
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'accounts/password_change_form.html', {'form': form, 'title': 'Change Your Password'})
    else:
        return redirect('home')