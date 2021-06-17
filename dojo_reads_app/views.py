from django.shortcuts import render, redirect
from .models import User, Book, Author, Review
from django.contrib import messages


# Create your views here.
def index(request):
    if not 'user_id' in request.session:
        return redirect("/")

    context = {
        'logged_user' : User.objects.get(id=request.session['user_id']),
        'all_books' : Book.objects.all(),
        'recent_reviews': Review.objects.order_by('-created_at')[:3]
    }

    return render(request, "books_index.html", context)


def add_book(request):
    if not 'user_id' in request.session:
        return redirect("/")
    
    context = {
        'all_authors': Author.objects.all()
    }

    return render(request, "add_book.html", context)


def create_book(request):
    if not 'user_id' in request.session:
        return redirect("/")

    if request.method == "POST":
        #errors handling
        book_errors = Book.objects.book_validator(request.POST)
        review_errors = Review.objects.review_validator(request.POST)
        errors = list(book_errors.values())+list(review_errors.values())

        if request.POST['author_id'] == "-1":
            if request.POST['author_name'] ==  "":
                messages.error(request, "Please either choose an author from the dropdown or create a new one")
            else:
                author_errors = Author.objects.author_validator(request.POST)
                errors+= list(author_errors.values())
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/books/add')

        #main method
        if request.POST['author_id'] == "-1":
            author = Author.objects.create(name = request.POST['author_name'])
        else: 
            author = Author.objects.get(id = request.POST['author_id'])
        this_book = Book.objects.create(title = request.POST['title'])
        logged_user = User.objects.get(id=request.session['user_id'])
        Review.objects.create(
            content = request.POST['content'], 
            rating = int(request.POST['rating']),
            reviewed_by = logged_user, 
            book_reviewed = this_book, 
        )
        this_book.authors.add(author)
        return redirect(f'/books/{this_book.id}')
    else:
        return redirect("/books/add")


def display_book(request, book_id):
    if not 'user_id' in request.session:
        return redirect("/")

    context = {
        'book' : Book.objects.get(id=book_id)
    }
    return render(request, 'display_book.html', context)


def add_review(request):
    if not 'user_id' in request.session:
        return redirect("/")

    book_to_review = Book.objects.get(id=request.POST['book_id'])
    if request.method == "POST":
        #errors handling
        errors = Review.objects.review_validator(request.POST)
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
        else:
            logged_user = User.objects.get(id=request.session['user_id'])
            Review.objects.create(
                content = request.POST['content'], 
                rating = int(request.POST['rating']),
                reviewed_by = logged_user, 
                book_reviewed = book_to_review, 
            )
    return redirect(f"/books/{book_to_review.id}")


        
    return redirect(f"/books/{book_to_review.id}")


def delete_review(request):
    if not 'user_id' in request.session:
        return redirect("/")
    
    book_to_view = Book.objects.get(id=request.POST['book_id'])
    if request.method == "POST":
        review_to_delete = Review.objects.get(id=request.POST['review_id'])
        review_to_delete.delete()
    return redirect(f"/books/{book_to_view.id}")
    

