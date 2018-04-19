from django.shortcuts import render

# Create your views here.
from Dashboard.models import SpecificNotification


def notify_users(notification_type, message, heading, user, action="Nothing for now"):
    if notification_type == 'specific':
        notification_objs = []
        for each_user in user:
            notification_objs.append(
                SpecificNotification(user=each_user, action=action, notification=message, heading=heading))

        SpecificNotification.objects.bulk_create(notification_objs)
    elif notification_type == "general":
        print("General Notification")

    else:
        print("Should not go here:General\\views")
