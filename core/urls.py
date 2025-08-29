from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                  # homepage
    path('logout/', views.logout_now, name='logout_now'),
      path("logout/", views.logout_now, name="logout"),  # GET logout -> home
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('travels/', views.TravelListView.as_view(), name='travel_list'),
    path('travels/<int:pk>/', views.TravelDetailView.as_view(), name='travel_detail'),
    path('travels/<int:pk>/book/', views.create_booking, name='create_booking'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path("bookings/<int:pk>/cancel/", views.cancel_booking, name="cancel_booking"),
]
