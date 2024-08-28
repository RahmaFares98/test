from django.urls import path
from . import views

urlpatterns = [
    #main website pages
    path('', views.home, name='home'),
    path('about-us', views.about_us, name='about_us'),
    path('services', views.services, name='services'),
    path('contact-us', views.contact_us, name='contact_us'),

    #Sign in, up, and out paths
    path('sign-in', views.sign_in, name='sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('sign-out', views.sign_out, name='sign_out'),
    
    # #admin pages and CRUD operations
    # path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    # path('create-company', views.create_company, name='create_company'),
    # path('update-company', views.update_company, name='update_company'),
    # path('view-all-companies', views.view_companies, name='view_companies'),

    #Company pages and CRUD operations
    path('company-dashboard', views.company_dashboard_view, name='company_dashboard'),
    path('create-order', views.create_order, name='create_order'),
    path('update-order', views.update_order, name='update_order'),
    path('view-all-orders', views.view_orders, name='view_orders'),

    # CRUD operation for Orders
    path('company-create-order', views.company_create_order, name='company_create_order'),
    path('company-update-order/edit/<int:order_id>', views.company_edit_order, name='company_edit_order'),
    path('company-orders', views.company_orders, name='company_orders'),
    path('company-orders/', views.company_orders_view, name='company_orders'),
    path('company-orders/delete/<int:order_id>/', views.company_delete_order_view, name='company_delete_order'),


    #CRUD operations for Customers
    path('company-create-customer', views.company_create_customer, name='company_create_customer'),
    path('company-update-customer/edit/<int:customer_id>', views.company_edit_customer, name='company_edit_customer'),
    path('compant-customers', views.company_customers, name='company_customers'),
    path('company-customers/', views.company_customers_view, name='company_customers'),
    path('company-customers/delete/<int:customer_id>/', views.company_delete_customer_view, name='company_delete_customer'),

    #CRUD operations for Delivery Drivers
    path('company-create-driver', views.company_create_driver, name='company_create_driver'),
    path('company-update-driver/edit/<int:driver_id>', views.company_edit_driver, name='company_edit_driver'),
    path('compant-driver', views.company_drivers, name='company_drivers'),
    path('company-drivers/', views.company_drivers_view, name='company_drivers'),
    path('company-drivers/delete/<int:driver_id>/', views.company_delete_driver_view, name='company_delete_driver'),



    
     # Admin Dashboard
    path('admindashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('adminusers/', views.admin_users_view, name='admin_users'),
    path('adminusers/edit/<int:user_id>/', views.admin_user_edit_view, name='admin_user_edit'),
    path('adminusers/delete/<int:user_id>/', views.admin_delete_user_view, name='admin_delete_user'),

    path('admincompanies/', views.admin_companies_view, name='admin_companies'),
    path('admincompanies/edit/<int:company_id>/', views.admin_company_edit_view, name='admin_company_edit'),
    path('admincompanies/delete/<int:company_id>/', views.admin_company_delete_view, name='admin_company_delete'),

    path('adminorders/', views.admin_orders_view, name='admin_orders'),
    path('adminorders/detail/<int:order_id>/', views.admin_order_detail_view, name='admin_order_detail'),
    path('adminuorders/edit/<int:order_id>/', views.admin_order_edit_view, name='admin_order_edit'),
    path('adminorders/delete/<int:order_id>/', views.admin_order_delete_view, name='admin_order_delete'),

    path('salesdata/', views.sales_data, name='sales_data'),

  

    #create company and customer from the admin side:
    path('admin-create-company', views.admin_create_comapny , name="admin_create_comapny"),
    path('admin-create-customer', views.admin_create_customer , name="admin_create_customer"),
    

    #Tracking Order Map:
    path('admin-tracking-order', views.admin_tracking_order, name='admin_tracking_order'),
    path('admin-tracking-order-view/<int:order_id>/', views.admin_tracking_order_view, name='admin_tracking_order_view'),

    path('company-tracking-order', views.company_tracking_order, name="company_tracking_order"),

    #notifications path:
    path('notifications/', views.fetch_notifications, name='fetch_notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),


    #chatbot path
    path('chatbot', views.chatbot_page, name='chatbot_page'),
    path('get-response', views.get_response, name='get_response'),
    
    #Report and download pdf file path
    path('admin-reports', views.admin_reports, name='admin_reports'),
    path('company-reports', views.company_reports, name='company_reports'),


    #pdf file:
    path('download-pdf', views.download_pdf, name= 'download_pdf'),
    path('users-download-pdf', views.users_download_pdf, name= 'users_download_pdf'),

    





    
]
