from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path("book-room/<int:room_id>/", views.book_room, name="book_room"),
    path("payment/<int:booking_id>/", views.payment_page, name="payment_page"),
    path("payment-success/", views.payment_success, name="payment_success"),
    # path('bookings/', views.book_room, name='book_room'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('hotel/mpesaPayments', views.mpesaPayments, name='mpesaPayments'),
  ]  
    
   