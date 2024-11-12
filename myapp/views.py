# views.py
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import get_user_model,authenticate,login
from .forms import CarForm,BookingForm
from .models import Car,Booking
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import date
from django.db.models import Q
def home(request):
    return render(request,'home.html')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        # Create the user
        User = get_user_model()
        user = User.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        if user is not None:
            login(request,user)
            return redirect('home')
        # Redirect to a success page or do something else
    return render(request, 'register.html')
def customer_login(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            User = get_user_model()
            user1=User.objects.get(username=username)
            if user1.user_type == 'customer':
             login(request,user)
             # context={"user":user}
             return redirect('customer_home')
    return render(request,'customer_login.html')
def dealer_login(request):
    if request.method == 'POST' :
       username = request.POST.get('username')
       password = request.POST.get('password')
       user=authenticate(username=username,password=password)
       if user is not None:
            User = get_user_model()
            user1=User.objects.get(username=username)
            if user1.user_type == 'dealer':
             login(request,user)
              # context={"user":user}
             return redirect('vehicle_list')
    return render(request,'dealer_login.html')
def add_car(request):
    if request.method == 'POST':
       form=CarForm(request.POST,request.FILES)
       if form.is_valid():
           car=form.save(commit=False)
           car.car_dealer=request.user
           car.save()
           return redirect('vehicle_list')
    #    else:
    #        print(form.errors)
    #        print("invalid")
    else:
        form=CarForm()   
    return render(request,'add_car.html',{"form":form,"user":request.user})
def customer_home(request):
    user = request.user
    cars = Car.objects.all()  # Fetch all cars, adjust the queryset as needed
    model_search = request.GET.get('model_search')
    if model_search:
        cars = cars.filter(Q(model__icontains=model_search))
    context = {
        'user': user,
        'cars': cars,
    }
    return render(request, 'customer_home.html', context)
def added(request):
    return render(request,'added.html')
def dealer_home(request):
    return render(request,'dealer_home.html')
def vehicle_list(request):
    cur_dealer=request.user;
    cars=Car.objects.filter(car_dealer = cur_dealer)
    return render(request,'vehicle_list.html',{"cars":cars})
def edit(request, car_id):
    car=Car.objects.get(id = car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
        else:
            print(form.errors)
    else:
        form = CarForm(instance=car)
    return render(request, 'edit.html', {'form': form})
def book_car(request, car_id):
    car =   Car.objects.get(id = car_id)
    print(car.model)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            if booking_date < date.today():
                return render(request, 'book_car.html', {"msg": "Invalid date. Please choose a future date."})
            if not Booking.objects.filter(car=car, booking_date=booking_date).exists():
                booking = form.save(commit=False)
                booking.car = car
                booking.customer = request.user
                booking.status = 'Pending'  # Initial status is set to Pending
                booking.save()
                dealer_email = car.car_dealer.email
                subject = 'New Booking Request'
                context = {'car_model': car.model, 'booking_date': booking_date,"car_rent":car.rent}
                message = render_to_string('email.html', context)
                plain_message = strip_tags(message)
                send_mail(subject, plain_message, 'rentwise.info@gmail.com', [dealer_email], html_message=message)
                # messages.success(request, 'Booking request sent! Waiting for dealer confirmation.')
                return redirect('customer_dashboard')
            else:
                return render(request,'book_car.html',{"msg":"Not available"})
                # messages.error(request, 'Selected date is not available. Please choose a different date.')
    else:
        form = BookingForm()
    print(car)    
    return render(request, 'book_car.html', {'form': form, 'car': car})
def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})
def dealer_bookings(request):
    dealer = request.user
    bookings = Booking.objects.filter(car__car_dealer=dealer)
    return render(request, 'all_orders.html', {'bookings': bookings})
def customer_dashboard(request):
    customer = request.user
    bookings = Booking.objects.filter(customer=customer)
    return render(request, 'customer_dashboard.html', {'bookings': bookings})
# bookings/views.py
def accept_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
      booking.status = 'Accepted'
      booking.save()
      car_model = booking.car.model
      booking_date = booking.booking_date
      car_rent = booking.car.rent
      customer_email = booking.customer.email
      subject = 'Booking Accepted'
      context = {'car_model': car_model, 'booking_date': booking_date, 'car_rent': car_rent}
      message = render_to_string('customer_email.html', context)
      plain_message = strip_tags(message)
      send_mail(subject, plain_message, 'rentwise.info@gmail.com', [customer_email], html_message=message)
    return redirect('all_orders')
def reject_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        # Additional logic for dealer actions (e.g., check availability, set status, etc.)
        booking.status = 'Rejected'
        booking.save()
        booking.delete()
        car_model = booking.car.model
        booking_date = booking.booking_date
        car_rent = booking.car.rent
        customer_email = booking.customer.email
        subject = 'Booking Rejected'
        context = {'car_model': car_model, 'booking_date': booking_date,}
        message = render_to_string('reject_email.html', context)
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, 'rentwise.info@gmail.com', [customer_email], html_message=message)
    return redirect('all_orders')
