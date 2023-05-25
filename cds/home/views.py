from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request, 'home/index.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        subject = 'Contact Form Submission'
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])

        # You can add further logic here, such as displaying a success message
        # or redirecting the user to a thank you page.

    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')