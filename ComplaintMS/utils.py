# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_complaint_notification(complaint):
    subject = f'New Complaint Submitted: {complaint.Subject}'
    message = f"""
    A new complaint has been submitted by {complaint.user.username}.
    
    Details:
    Subject: {complaint.Subject}
    Type: {complaint.Type_of_complaint}
    Description: {complaint.Description}
    Address: {complaint.address}
    Time: {complaint.Time}
    
    Please take necessary actions.
    """
    
    recipient_list = ['harisharma00456@gmail.com']  # Replace with the actual staff email

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

def send_status_change_notification(complaint):
    subject = f'Your Complaint Status has been Updated: {complaint.Subject}'
    message = f"""
    Dear {complaint.user.username},
    
    The status of your complaint has been updated.
    
    Details:
    Subject: {complaint.Subject}
    Type: {complaint.Type_of_complaint}
    Description: {complaint.Description}
    Address: {complaint.address}
    Time: {complaint.Time}
    Status: {complaint.get_status_display()}
    
    Thank you for your patience.
    """

    recipient_list = [complaint.user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )