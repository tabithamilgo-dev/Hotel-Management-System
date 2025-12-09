from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Room, Booking
from django.contrib.auth.models import User
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from .models import ContactMessage


# Create your views here.
# Home page
def home(request):
    rooms = Room.objects.all() 
    return render(request, 'home.html', {'rooms': rooms})

# Rooms page
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

# Book room page
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if Booking.objects.filter(room=room).exists():
        messages.error(request, "This room is already booked. Please choose another room.")
        return redirect("rooms")

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")

        booking = Booking.objects.create(
            room=room,
            guest_name=name,
            guest_email=email,
            check_in=checkin,
            check_out=checkout,
        )

        messages.success(request, "Room booked successfully!")
        return redirect("payment_page", booking_id=booking.id)

    return render(request, "book_room.html", {"room": room})

# Payment page
def payment_page(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":
        booking.is_paid = True
        booking.save()

        return redirect("payment_success")

    return render(request, "payment.html", {"booking": booking})

def payment_success(request):
    return render(request, "payment_success.html")

# contact us page
def contact(request):
    return render(request, 'contact.html')

# User registration
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "registration/register.html")

# M-Pesa payment processing
def mpesaPayments(request):
    response = None  
    if request.method == "POST":
        phoneNumber = request.POST.get("phone_number")
        amount = int(request.POST.get("amount"))
         
        cl = MpesaClient()
        accountReference = 'hotel'
        transactionDesc = 'hotel payments'
        callbackUrl = 'https://api.darajambili.com/express-payment'

        response = cl.stk_push(phoneNumber, amount,
                               accountReference, transactionDesc, callbackUrl)

    return render(request, 'mpesa_payments.html', {'response': response})


# Contact us page
def contact(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message)
        success = True

    return render(request, "contact.html", {"success": success})
