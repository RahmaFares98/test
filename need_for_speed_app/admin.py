from django.contrib import admin
from .models import *
from .models import User, Order, Notification, Customer, Delivery, Company, Location
# Register your models here.

# admin.site.register(User)
# admin.site.register(Order)
# admin.site.register(Customer)
# admin.site.register(Delivery)
# admin.site.register(Company)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'role')
    list_filter = ('role',)
    ordering = ('-created_at',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number','number_of_workers', 'email')
    search_fields = ('company_name',  'phone_number','email')
    ordering = ('company_name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'phone_number', 'status')
    search_fields = ('first_name','last_name' ,'name', 'phone_number' )
    ordering = ('first_name','last_name',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'license', 'status', 'worklocation')
    search_fields = ('first_name', 'last_name', 'license', 'worklocation')
    list_filter = ('status',)
    ordering = ('first_name',)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_name', 'customer', 'company', 'pickup_location', 'pickoff_location', 'order_status', 'created_at')
    search_fields = ('order_name', 'customer__name', 'company__name')
    list_filter = ('order_status',)
    ordering = ('-created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'link', 'action', 'object_id', 'message','is_read', 'created_at' )
    search_fields = ('user', 'message')
    list_filter = ('is_read',)
    ordering = ('-created_at',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('house', 'name', 'zipcode', 'city', 'country', 'address', 'created_at', 'updated_at')
    search_fields = ('name', 'city', 'country', 'address')
    list_filter = ('city', 'country', 'address')
    ordering = ('-created_at',)
    

# Customizing the admin site's appearance
admin.site.site_header = "Need for Speed Admin"
admin.site.site_title = "Need for Speed Admin Portal"
admin.site.index_title = "Welcome to Need for Speed Administration"