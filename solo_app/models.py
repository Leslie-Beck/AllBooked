from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        first_name = reqPOST['first_name'] 
        last_name = reqPOST['last_name']
        if not first_name.isalpha() & last_name.isalpha():
            errors['letters_only'] = "First and Last name can only contain letters"
        if len(first_name) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(last_name) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if reqPOST['password'] != reqPOST['conf_password']:
            errors['match'] = "Password and Password Confirmation don't match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Invalid email address!"
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email) >=1:
            errors['dup'] = "Email taken, use another"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = UserManager()


class BookManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['title']) < 1:
            errors['title'] = "Book Field cannot be empty"
        book_with_name = Book.objects.filter(title=reqPOST['title'])
        if len(book_with_name) >=1:
            errors['dup'] = "This title has already been taken, please choose another."
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    reviews = models.ForeignKey('Review', related_name="reviews", null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = BookManager()

class ReviewManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['review']) <5:
            errors['review'] = "review must be at least 5 characters!"
        return errors

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    book_reviewed = models.ForeignKey(Book, related_name="review_for_book", on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name="reviews_uploaded", null=True, on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ReviewManager()

class Comment(models.Model):
    comment = models.TextField()
    posted_by = models.ForeignKey(User, related_name="comments_posted", on_delete=models.CASCADE)
    posted_on = models.ForeignKey(Review, related_name="comments_on", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)