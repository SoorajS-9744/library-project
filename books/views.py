from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User


@never_cache
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")




@login_required
@never_cache
def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})




@login_required
@never_cache
def add_book(request):
    if request.method == "POST":
        book_name = request.POST.get("book_name")
        author = request.POST.get("author")
        pub_date = request.POST.get("pub_date")
        rate = request.POST.get("rate")

        Book.objects.create(
            book_name=book_name,
            author=author,
            pub_date=pub_date,
            rate=rate
        )

        return redirect("home")

    return render(request, "add_book.html")



@login_required
@never_cache
def update_book(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        book.book_name = request.POST.get("book_name")
        book.author = request.POST.get("author")
        book.pub_date = request.POST.get("pub_date")
        book.rate = request.POST.get("rate")

        book.save()

        return redirect("home")

    return render(request, "update_book.html", {"book": book})


@login_required
@never_cache
def delete_book(request, id):
    book = Book.objects.get(id=id)

    book.delete()

    return redirect('home')



def logout_view(request):
    logout(request)
    return redirect("login")



def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "signup.html")