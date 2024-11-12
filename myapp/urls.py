from django.urls import path
from . import views 
urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('customerlogin',views.customer_login,name='customer_login'),
    path('dealerlogin',views.dealer_login,name='dealer_login'),
    path('addcar',views.add_car,name='add_car'),
    path('customerhome',views.customer_home,name='customer_home'),
    path('added',views.added,name='added'),
    path('dealerhome',views.dealer_home,name='dealer_home'),
    path('vehiclelist',views.vehicle_list,name='vehicle_list'),
    path('edit/<int:car_id>',views.edit,name='edit'),
    path('book_car/<int:car_id>/',views.book_car,name='book_car'),
    path('booking_confirmation/<int:booking_id>/',views.booking_confirmation,name='booking_confirmation'),
    path('all_orders',views.dealer_bookings,name='all_orders'),
    path('accept_booking/<int:booking_id>/',views.accept_booking,name='accept_booking'),
    path('reject_booking/<int:booking_id>/',views.reject_booking,name='reject_booking'),
    path('customer_dashboard',views.customer_dashboard,name='customer_dashboard'),
    # path('customerhome',views.customer_home,name='customer_home'),
]
