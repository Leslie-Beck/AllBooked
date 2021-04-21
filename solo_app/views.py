from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            print(user.password)
            print(request.session['user_id'])
            return redirect('/users/profile')
    return redirect('/')

def register(request):
    return render(request, 'register.html')

def main_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_users': User.objects.all(),
        'all_books': Book.objects.all(),
        'all_reviews': Review.objects.all(),
    }
    return render(request, 'main_page.html', context)

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                print(user.password)
                return redirect('/users/profile')
        messages.error(request, "email or password are not correct")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def create_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Book.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/profile')
        else:
            book = Book.objects.create(title=request.POST['title'], uploaded_by=User.objects.get(id=request.session['user_id']))
            review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book_reviewed=book, uploaded_by=User.objects.get(id=request.session['user_id']))
    return redirect('/users/profile')

def create_ajax(request):
    if request.method == "POST":
        book = Book.objects.create(title=request.POST['title'], uploaded_by=User.objects.get(id=request.session['user_id']))
        review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book_reviewed=book, uploaded_by=User.objects.get(id=request.session['user_id']))
        context = {
            "all_books": Book.objects.all(),
            "all_reviews": Review.objects.all()
        }
        return render(request, "table_snippet.html", context)


def delete_book(request, book_id):
    if request.method == "POST":
        book_to_delete = Book.objects.get(id=book_id)
        if book_to_delete.uploaded_by.id == request.session['user_id']:
            book_to_delete.delete()
    return redirect('/users/profile')


def book_page(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    books_with_id = Book.objects.filter(id=book_id)
    if len(books_with_id) ==0:
        return redirect('/users/profile')
    context = {
        'this_book': Book.objects.get(id=book_id), 
        'all_users': User.objects.all(),
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_reviews': Review.objects.filter(book_reviewed=book_id),
        'all_comments': Comment.objects.all(),
    }
    return render(request, 'book_page.html', context)

def review_others_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Review.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/profile')
        else:
            review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book_reviewed=Book.objects.get(id=book_id), uploaded_by=User.objects.get(id=request.session['user_id']))
            return redirect(f'/books/{book_id}')
    return redirect('/users/profile')


def post_comment(request, book_id, review_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        poster = User.objects.get(id=request.session['user_id'])
        review = Review.objects.get(id=review_id)
        Comment.objects.create(comment=request.POST['comment'], posted_by=poster, posted_on=review)
    return redirect(f'/books/{book_id}')


def like(request, book_id, review_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        this_review = Review.objects.get(id=review_id)
        current_user = User.objects.get(id=request.session['user_id'])
        this_review.users_who_like.add(current_user)
    return redirect(f'/books/{book_id}')

def unlike(request, book_id, review_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        this_review = Review.objects.get(id=review_id)
        current_user = User.objects.get(id=request.session['user_id'])
        this_review.users_who_like.remove(current_user)
    return redirect(f'/books/{book_id}')