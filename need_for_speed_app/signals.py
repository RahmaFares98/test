from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notification, User, Order

# @receiver(post_save, sender=Order)
# def create_order_notification(sender, instance, created, **kwargs):
#     if created:
#         # Notify admins
#         admins = User.objects.filter(role='admin')
#         for admin in admins:
#             Notification.objects.create(
#                 user=admin,
#                 content_type='Order',
#                 action='created',
#                 message=f'New order created: {instance.order_name} with code {instance.order_code_number}',
#                 link=f'/orders/{instance.id}'
#             )

#         # Notify companies
#         if instance.company:
#             Notification.objects.create(
#                 user=instance.company,
#                 content_type='Order',
#                 action='created',
#                 message=f'New order created: {instance.order_name} with code {instance.order_code_number}',
#                 link=f'/orders/{instance.id}'
#             )

# @receiver(post_save, sender=Order)
# def update_order_notification(sender, instance, **kwargs):
#     if not kwargs.get('created', False):
#         # Notify admins
#         admins = User.objects.filter(role='admin')
#         for admin in admins:
#             Notification.objects.create(
#                 user=admin,
#                 content_type='Order',
#                 action='updated',
#                 message=f'Order updated: {instance.order_name} with code {instance.order_code_number}',
#                 link=f'/orders/{instance.id}'
#             )

#         # Notify companies
#         if instance.company:
#             Notification.objects.create(
#                 user=instance.company,
#                 content_type='Order',
#                 action='updated',
#                 message=f'Order updated: {instance.order_name} with code {instance.order_code_number}',
#                 link=f'/orders/{instance.id}'
#             )

# @receiver(post_delete, sender=Order)
# def delete_order_notification(sender, instance, **kwargs):
#     # Notify admins
#     admins = User.objects.filter(role='admin')
#     for admin in admins:
#         Notification.objects.create(
#             user=admin,
#             content_type='Order',
#             action='deleted',
#             message=f'Order deleted: {instance.order_name} with code {instance.order_code_number}',
#             link=f'/orders/{instance.id}'
#         )

#     # Notify companies
#     if instance.company:
#         Notification.objects.create(
#             user=instance.company,
#             content_type='Order',
#             action='deleted',
#             message=f'Order deleted: {instance.order_name} with code {instance.order_code_number}',
#             link=f'/orders/{instance.id}'
#         )

# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import *

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        # Notify admins
        admins = User.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                user=admin,
                content_type='Order',
                action='created',
                message=f'New order created: {instance.order_name} with code {instance.order_code_number}',
                link=f'/adminorders/detail/{instance.id}/'  # Updated link to order detail page
            )

        # Notify companies
        if instance.company:
            Notification.objects.create(
                user=instance.company,
                content_type='Order',
                action='created',
                message=f'New order created: {instance.order_name} with code {instance.order_code_number}',
                link=f'/adminorders/detail/{instance.id}/'  # Updated link to order detail page
            )

@receiver(post_save, sender=Order)
def update_order_notification(sender, instance, **kwargs):
    if not kwargs.get('created', False):
        # Notify admins
        admins = User.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                user=admin,
                content_type='Order',
                action='updated',
                message=f'Order updated: {instance.order_name} with code {instance.order_code_number}',
                link=f'/adminorders/detail/{instance.id}/'  # Updated link to order detail page
            )

        # Notify companies
        if instance.company:
            Notification.objects.create(
                user=instance.company,
                content_type='Order',
                action='updated',
                message=f'Order updated: {instance.order_name} with code {instance.order_code_number}',
                link=f'/adminorders/detail/{instance.id}/'  # Updated link to order detail page
            )

@receiver(post_delete, sender=Order)
def delete_order_notification(sender, instance, **kwargs):
    # Notify admins
    admins = User.objects.filter(role='admin')
    for admin in admins:
        Notification.objects.create(
            user=admin,
            content_type='Order',
            action='deleted',
            message=f'Order deleted: {instance.order_name} with code {instance.order_code_number}',
            link=f'/adminorders/detail/{instance.id}/'  # Updated link to order detail page (might show a "deleted" notice)
        )

    # Notify companies
    if instance.company:
        Notification.objects.create(
            user=instance.company,
            content_type='Order',
            action='deleted',
            message=f'Order deleted: {instance.order_name} with code {instance.order_code_number}',
            link=f'/company-orders/detail/{instance.id}/'  # Updated link to order detail page (might show a "deleted" notice)
        )