from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse , JsonResponse, FileResponse
import bcrypt
import requests
from django.urls import reverse
from django.db.models import Count
from datetime import timedelta
from datetime import datetime
from django.utils import timezone
from .models import User, Customer, Company, Delivery, Order, Notification, Location
from .utils import get_coordinates
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import landscape, A4
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors



# Create your views here.

# def download_pdf(request):
#     buf = io.BytesIO()
#     canv = canvas.Canvas(buf, pagesize=letter, bottomup = 0)
#     textob = canv.beginText()
#     textob.setTextOrigin(inch, inch)
#     textob.setFont("Helvetica", 14)

#     lines = []

#     orders = Order.objects.all()

#     for order in orders:
#         lines.append(f"Order ID: {order.id}")
#         lines.append(f"Order Name: {order.order_name}")
#         lines.append(f"Order Serial Number: {order.order_code_number}")
#         lines.append(f"Pick Up Location: {order.pickup_location}")
#         lines.append(f"Drop Off Location: {order.pickoff_location}")
#         lines.append(f"Total: {order.Total}")
#         lines.append(f"Customer Name: {order.customer.first_name} {order.customer.last_name}")
#         lines.append(f"Company Name: {order.company.company_name}")
#         lines.append(f"Order Status: {order.order_status}")
#         lines.append(f"Created At: {order.created_at}")
#         lines.append(f"Updated At: {order.updated_at}")
#         lines.append(" ")  # Empty line for spacing

#     for line in lines:
#         textob.textLine(line)   


#     canv.drawText(textob)
#     canv.showPage() 
#     canv.save()
#     buf.seek(0)   

#     return FileResponse(buf, as_attachment =True, filename= 'all-orders.pdf')
def download_pdf(request):
    buf = io.BytesIO()
    
    # Use landscape A4 page size
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4))
    elements = []

    data = [
        ["Order Name", "Order Serial Number", "Pick Up Location", "Drop Off Location", "Total", "Customer Name", "Company Name", "Company Email", "Order Status"]
    ]

    orders = Order.objects.all()
    
    for order in orders:
        data.append([
            # order.id,
            order.order_name,
            order.order_code_number,
            order.pickup_location,
            order.pickoff_location,
            order.Total,
            f"{order.customer.first_name} {order.customer.last_name}",
            order.company.company_name,
            order.company.email,
            order.order_status,
            # order.created_at,
            # order.updated_at
        ])

    table = Table(data)
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    table.setStyle(style)
    
    elements.append(table)

    doc.build(elements)
    
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='all-orders.pdf')


def users_download_pdf(request):
    buf = io.BytesIO()

    # Set the page size to A4 
    doc = SimpleDocTemplate(buf, pagesize=A4)
    elements = []

    # Define table data and headers
    data = [
        ["User ID", "First Name", "Last Name", "Address", "Phone Number", "Created At"]
    ]

    # Fetch users from the database
    users = User.objects.all()
    for user in users: 
        created_at_formatted = user.created_at.strftime('%d-%m-%Y') 
        
        data.append([
            user.id,
            user.first_name,
            user.last_name,
            user.address,
            user.phone_number,
            created_at_formatted,
            # user.updated_at
        ])

    # Create a Table object
    table = Table(data)

    # Define the table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)

    # Add the table to the PDF elements list
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='all-users.pdf')

#main project nav pages
def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    return render(request, 'main/AboutUs.html')

def services(request):
    return render(request, 'main/Services.html')   

def contact_us(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # service_type = request.POST.get('service_type')
        comment = request.POST.get('comment')

        if not first_name or not last_name or not email:
            return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields'})

        subject = f"Contact Us Form Submission from {first_name} {last_name}"
        message = f"Service Type: {service_type}\n\nComment:\n{comment}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.CONTACT_EMAIL]  

        try:
            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse({'status': 'success', 'message': 'Your message has been sent successfully!'})
        except Exception as e:
            print(e)  
            return JsonResponse({'status': 'error', 'message': 'An error occurred while sending your message.'})

    return render(request, 'main/ContactUs.html')


#Sign in , Sign up, and Sign out Functions
def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email).first()
        
    
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['email'] = email
            request.session['user_id'] = user.id 
            if user.role == 'admin':
               
                messages.success(request, 'Welcome!')
                return redirect('admin_dashboard')
                # return render(request, 'admin/AdminDashboard.html', {'user': user})
            else:
                messages.success(request, 'Welcome!')
                return redirect('company_dashboard')
                # return render(request, 'company/CompanyDashboard.html', {'user': user})
        else:
            messages.error(request, 'Invalid email or password', extra_tags='sign_in')
            return redirect('sign_in')
        
    return render(request, 'main/SignIn.html')     


            
def sign_up(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='sign_up')
            return redirect('sign_up')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            role =request.POST.get('role')
            email = request.POST['email']
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number= phone_number,
                role = role,
                email=email,
                password=hashed_password
                )
            user.save()
            if user.role == 'admin':
                messages.success(request, 'Registration successful! Please log in.')
                return render(request, 'admin/AdminDashboard.html', {'user': user})
            else:
                messages.success(request, 'Registration successful! Please log in.')
                return render(request, 'company/CompanyDashboard.html', {'user': user})
    else:
        return render(request, 'main/SignUp.html') 

def sign_out(request):
    if request.method == 'POST':
        request.session.flush()# make sure all session data is securely removed
        messages.success(request, 'Logout successful!', extra_tags='sign_out')
        return redirect('home')
    return redirect('home')     
    



def admin_dashboard(request):
    return render(request, 'AdminDashboard.html')

def  create_company(request):
    return render(request, 'CreateComapny.html')

def  update_company(request):
    return render(request, 'UpdateComapny.html')

def  view_companies(request):
    return render(request, 'ViewAllComapnies.html')


def company_dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    drivers = Delivery.objects.all()

    context = {
        'customers': customers,
        'drivers': drivers,
        'orders': orders,
    }
    return render(request, 'company/CompanyDashboard.html')


def create_order(request):
    if request.method == 'POST':
        # Validate the input data (assuming you have a user_validator in User model)
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='create_order')
            return redirect('create_order')
        else:
            # Get the data from the POST request
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            company_name = request.POST['company_name']
            order_name = request.POST['order_name']
            order_code_number = request.POST['order_code_number']
            total = request.POST['Total']  # Use 'Total' instead of 'order_price'
            pickup_location = request.POST['pickup_location']
            pickoff_location = request.POST['pickoff_location']

            # Create the customer and company
            customer = User.objects.create(first_name=first_name, last_name=last_name, address=address, phone_number=phone_number)
            company = Company.objects.create(company_name=company_name, phone_number=phone_number)

            # Create the order and associate it with the customer and company
            order = Order.objects.create(
                order_name=order_name,
                company=company,
                order_code_number=order_code_number,
                pickup_location=pickup_location,
                pickoff_location=pickoff_location,
                Total=total,  
                customer=customer  # Assuming there's a relationship to the customer
            )

            # Send a success message and redirect
            messages.success(request, 'Your order has been created successfully')
            return redirect('create_order')
    else:
        return render(request, 'admin/CreateOrder.html')

def update_order(request):
    return render(request, 'admin/UpdateOrder.html') 

def view_orders(request):
    return render(request, 'admin/ViewAllOrders.html') 


# Admin Dashboard View
def admin_dashboard_view(request):
    users = User.objects.all()
    companies = Company.objects.all()
    orders = Order.objects.all()

    context = {
        'users': users,
        'companies': companies,
        'orders': orders,
    }
    
    return render(request, 'admin/AdminDashboard.html', context)

# User Management Views
def admin_users_view(request):
    users = User.objects.all()
    return render(request, 'admin/admin_user.html', {'users': users})

def admin_user_edit_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.adress = request.POST.get('address')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return redirect('admin_users')

    return render(request, 'admin/admin_user_edit.html', {'user': user})

def admin_delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_users')

# Company Management Views
def admin_companies_view(request):
    companies = Company.objects.all()
    return render(request, 'admin/admin_company.html', {'companies': companies})

def admin_company_edit_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        company.company_name = request.POST.get('company_name')
        company.address = request.POST.get('address')
        company.phone_number = request.POST.get('phone_number')
        company.email = request.POST.get('email')
        company.save()
        return redirect('admin_companies')

    return render(request, 'admin/admin_company_edit.html', {'company': company})

def admin_company_delete_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    return redirect('admin_companies')

# Order Management Views
def admin_orders_view(request):
    orders = Order.objects.all()
    return render(request, 'admin/admin_order.html', {'orders': orders})

def admin_order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/admin_order_detail.html', {'order': order})

def admin_order_delete_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin_orders')


# Order Management Views
def admin_orders_view(request):
    orders = Order.objects.all()
    return render(request, 'admin/admin_order.html', {'orders': orders})

def admin_order_edit_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Get the data from the form
        customer_name = request.POST.get('customer_name')
        order_status = request.POST.get('order_status')
        total_amount = request.POST.get('total_amount')
        
        # Update the related customer object
        if order.customer:
            # Split the full name into first and last name
            name_parts = customer_name.split(' ', 1)
            if len(name_parts) == 2:
                order.customer.first_name, order.customer.last_name = name_parts
            else:
                order.customer.first_name = name_parts[0]
                order.customer.last_name = ''
            order.customer.save()  # Save the related customer object
        
        # Update the order object
        order.order_status = order_status
        order.Total = int(total_amount)  # Ensure total_amount is an integer
        
        # Save the updated order
        order.save()
        
        # Redirect to the order list page
        return redirect('admin_orders')

    # Render the edit form with the current order details for GET requests
    return render(request, 'admin/admin_order_edit.html', {'order': order})


def admin_order_delete_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('admin_orders')


def sales_data(request):
    # Group orders by status and count them
    orders_by_status = Order.objects.values('order_status').annotate(count=Count('order_status'))

    # Prepare data for the chart
    labels = [order['order_status'] for order in orders_by_status]
    data = [order['count'] for order in orders_by_status]

    response_data = {
        "labels": labels,
        "datasets": [{
            "label": "Order Distribution by Status",
            "data": data,
            "backgroundColor": ["#D74F28 ", "#FF6F00 ", "#F5A623 ", "#8C5E3C ", "#6D4C41 "],
            "borderColor": ["#D74F28 ", "#FF6F00 ", "#F5A623 ", "#8C5E3C ", "#6D4C41 "],
            "borderWidth": 1
        }]
    }
    return JsonResponse(response_data)    

#Admin Create Company Function:
def admin_create_comapny(request):
    if request.method == 'POST':
         # Validate the input data 
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='admin_create_comapny')
            return redirect('admin_create_comapny')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            company_name = request.POST['company_name']
            number_of_workers = request.POST['number_of_workers']
            email= request.POST['email']

            # Create a company
            
            company = Company.objects.create(first_name=first_name, last_name=last_name, address=address,company_name=company_name, phone_number=phone_number, number_of_workers =number_of_workers, email= email )

             # Send a success message and redirect
            messages.success(request, 'Your Company has been created successfully')
            return redirect('admin_create_comapny')
    else:
        return render(request, 'admin/admin_create_comapny.html')

#Admin Create Customer Function:
def admin_create_customer(request):
    if request.method == 'POST':
         # Validate the input data 
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='admin_create_comapny')
            return redirect('admin_create_comapny')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            status = request.POST['status']

            # Create a customer
            
            customer = Customer.objects.create(first_name=first_name, last_name=last_name, address=address, phone_number=phone_number, status=status )

             # Send a success message and redirect
            messages.success(request, 'Your Company has been created successfully')
            return redirect('admin_create_customer')
    else:
        return render(request, 'admin/admin_create_customer.html')



# Company Dashboard View
def company_dashboard_view(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    drivers = Delivery.objects.all()

    context = {
        'customers': customers,
        'drivers': drivers,
        'orders': orders,
    }
    return render(request, 'company/CompanyDashboard.html', context)

#Company order Functions:

def company_create_order(request): 
    if request.method == 'POST':
        # Validate the input data 
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='company_create_order')
            return redirect('company_create_order')
        else:
            # Get the data from the POST request
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            company_name = request.POST['company_name']
            order_name = request.POST['order_name']
            order_code_number = request.POST['order_code_number']
            total = request.POST['Total']  
            pickup_location = request.POST['pickup_location']
            pickoff_location = request.POST['pickoff_location']

            # Create the customer and company
            customer = User.objects.create(first_name=first_name, last_name=last_name, address=address, phone_number=phone_number)
            company = Company.objects.create(company_name=company_name, phone_number=phone_number)

            # Create the order and associate it with the customer and company
            order = Order.objects.create(
                order_name=order_name,
                company=company,
                order_code_number=order_code_number,
                pickup_location=pickup_location,
                pickoff_location=pickoff_location,
                Total=total,  
                customer=customer  
            )

            # Send a success message and redirect
            messages.success(request, 'Your order has been created successfully')
            return redirect('company_orders')
    else:
        return render(request, 'company/company_create_order.html')

def company_orders_view(request):
    orders = Order.objects.all()
    return render(request, 'company/company_orders.html', {'orders': orders})

def company_edit_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('company_orders')

    if request.method == 'POST':
        # errors = Order.objects.order_validator(request.POST)
        # if errors:
        #     for key, value in errors.items():
        #         messages.error(request, value, extra_tags='company_edit_order')
        #     return redirect('company_edit_order', order_id=order_id)

        customer_name = request.POST.get('customer_name', '')
        total_amount = request.POST.get('total_amount', 0)
        pickup_location = request.POST.get('pickup_location', '')
        pickoff_location = request.POST.get('pickoff_location', '')
        order_status = request.POST.get('order_status', order.order_status)
        

        # Update the related customer object
        if order.customer:
            name_parts = customer_name.split(' ', 1)
            if len(name_parts) == 2:
                order.customer.first_name, order.customer.last_name = name_parts
            else:
                order.customer.first_name = name_parts[0]
                order.customer.last_name = ''
                order.customer.save()
        
        # Update the order object
        order.order_status = order_status
        order.Total = int(total_amount) 
        order.pickup_location = pickup_location
        order.pickoff_location = pickoff_location

        order.save()

        messages.success(request, 'Order updated successfully')
        return redirect('company_orders')

    return render(request, 'company/company_edit_order.html', {'order': order})


def company_delete_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('company_orders')    

def company_orders(request):
    return render(request , 'company/company_orders.html')  

 


#Company customer Functions:
def company_create_customer(request): 
    if request.method == 'POST':
        # Validate the input data 
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='company_create_customer')
            return redirect('company_create_customer')
        else:
            # Get the data from the POST request
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
           

            # Create the customer and company
            customer = Customer.objects.create(first_name=first_name, last_name=last_name, address=address, phone_number=phone_number)

            customer.save()
            # Send a success message and redirect
            messages.success(request, 'Your order has been created successfully')
            return redirect('company_customers')
    else:
        return render(request, 'company/company_create_customer.html')

def company_customers_view(request):
    customers = Customer.objects.all()
    return render(request, 'company/company_customers.html', {'customers': customers}) 


def company_edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.address = request.POST.get('address')
        customer.phone_number = request.POST.get('phone_number')
        customer.save()
        return redirect('company_customers')
    return render(request , 'company/company_edit_customer.html', {'customer':customer})

def company_delete_customer_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect('company_customers')     

def company_customers(request):
    
    return render(request , 'company/company_customers.html')  

#Company driver Functions:

def company_create_driver(request): 
    if request.method == 'POST':
        # Validate the input data 
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='company_create_driver')
            return redirect('company_create_driver')
        else:
            # Get the data from the POST request
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            license =request.POST['license']
            status =request.POST['status']
            worklocation = request.POST['worklocation']

            # Create the Delivery Driver
            driver = Delivery.objects.create(first_name=first_name, last_name=last_name, address=address, phone_number=phone_number, license=license, status=status,worklocation=worklocation)


            # Send a success message and redirect
            messages.success(request, 'Your Delivery Driver has been created successfully')
            return redirect('company_drivers')
    else:
        return render(request, 'company/company_create_driver.html')

def company_drivers_view(request):
    drivers = Delivery.objects.all()
    return render(request, 'company/company_drivers.html', {'drivers': drivers}) 


def company_edit_driver(request, driver_id):
    driver = get_object_or_404(Delivery, id=driver_id)

    if request.method == 'POST':
        driver.first_name = request.POST.get('first_name')
        driver.last_name = request.POST.get('last_name')
        driver.address = request.POST.get('address')
        driver.phone_number = request.POST.get('phone_number')
        driver.license = request.POST.get('license')
        driver.status = request.POST.get('status')
        driver.worklocation = request.POST.get('worklocation')

        driver.save()
        return redirect('company_drivers')
    return render(request , 'company/company_edit_driver.html', {'driver': driver})

def company_delete_driver_view(request, driver_id):
    driver = get_object_or_404(Delivery, id=driver_id)
    driver.delete()
    return redirect('company_drivers')        

def company_drivers(request):
    return render(request , 'company/company_drivers.html')          

#Tracting Order On Google Map:
def admin_tracking_order(request):
    return render(request, 'admin/AdminTrackingPage.html') 

def get_coordinates(address):
    api_key = 'AAA_MAPS_API'  
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    results = response.json().get('results')
    if results:
        location = results[0].get('geometry', {}).get('location', {})
        return location.get('lat'), location.get('lng')
    return None, None 

def admin_tracking_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pickup_lat, pickup_lng = get_coordinates(order.pickup_location)
    dropoff_lat, dropoff_lng = get_coordinates(order.pickoff_location)

    context = {
        'order': order,
        'pickup_lat': pickup_lat,
        'pickup_lng': pickup_lng,
        'dropoff_lat': dropoff_lat,
        'dropoff_lng': dropoff_lng,
    }

    return render(request, 'admin/AdminTrackingPage.html', context)


def company_tracking_order(request):
    return render(request, 'company/CompanyTrackingPage.html')        


#Notifications Part:
def fetch_notifications(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        print("User is not authenticated. No user_id in session.")
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    print(f"User is authenticated with user_id: {user_id}")
    notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
    data = [{
        'id': notification.id,
        'message': notification.content_type,
        'read': notification.is_read,
        'link': notification.link
    } for notification in notifications]
    return JsonResponse(data, safe=False)

def notification_list(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('sign_in')  # Ensure 'login' points to your actual sign-in view name
    
    notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()  # Ensure this field name matches your model
    
    return render(request, 'admin_dashboard.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
def company_notification_list(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('sign_in')  # Ensure 'login' points to your actual sign-in view name
    
    notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()  # Ensure this field name matches your model
    
    return render(request, 'company_dashboard.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })    

def mark_notification_as_read(request, notification_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)
    
    try:
        notification = Notification.objects.get(id=notification_id, user_id=user_id)
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)





# chatbot functions:

def chatbot_page(request):
    return render(request, 'main/chatbot.html')

# def get_response(request):
#     userMessage = request.GET.get('userMessage')
#     return HttpResponse(userMessage)

def get_response(request):
    user_message = request.GET.get('userMessage', '').strip().lower()

    # Define predefined responses
    responses = {
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! How can I help you today?",
        "i want to ask you few questions about your website": "Sure! Here are some questions you can ask:\n1. What areas do you serve?\n2. How can I place an order?\n3. How do I track my delivery?\n4. Can I schedule a delivery for a specific time?\n5. How do I update my delivery address?",
        "what areas do you serve?": "We currently provide delivery services in [List of Areas or Cities]. If you’re unsure whether we deliver to your location, please enter your address on our website or contact our customer support team for assistance.",
        "how can i place an order?": "You can place an order by visiting our website or mobile app. Simply choose your items, select your delivery options, and complete the checkout process. If you need any help, feel free to reach out to our customer support.",
        "how do i track my delivery?": "Once your order is placed, you will receive a tracking link via email or SMS. You can use this link to monitor the real-time status and location of your delivery.",
        "can i schedule a delivery for a specific time?": "Yes, you can schedule your delivery for a specific time and date during the checkout process. Please ensure to place your order well in advance to accommodate your preferred delivery window.",
        "how do i update my delivery address?": "If you need to update your delivery address, please do so through your account on our website or app before finalizing your order. If your order has already been placed, contact our customer support team as soon as possible to make changes."
    }

    # Get the response based on the user message
    response_message = responses.get(user_message, "Sorry, I didn't understand that. Can you please rephrase your question?")

    return JsonResponse(response_message, safe=False)



def admin_reports(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    drivers = Delivery.objects.all()
    company =Company.objects.all()
    users = User.objects.all()

    context = {
        'customers': customers,
        'drivers': drivers,
        'orders': orders,
        'company':company,
        'users':users,
    }


    return render(request, 'admin/AdminReports.html', context)    

 
def company_reports(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    drivers = Delivery.objects.all()

    context = {
        'customers': customers,
        'drivers': drivers,
        'orders': orders,
    }


    return render(request, 'company/CompanyReports.html', context)     



     


      