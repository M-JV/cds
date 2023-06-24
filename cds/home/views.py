from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from cancer.ml import predict_tumor
from .forms import TumorDetectionForm
from cancer.models import TrainingData

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

def cancer(request):
    form = TumorDetectionForm()
    return render(request, 'home/cancer.html', {'form': form})

def prediction(request):
    if request.method == 'POST':
        form = TumorDetectionForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            result = predict_tumor(image)

            # Add training data
            training_data = TrainingData(image=image, prediction_result=str(result))
            training_data.save()

            return render(request, 'home/cancer.html', {'result': result})
    else:
        form = TumorDetectionForm()

    return render(request, 'home/cancer.html', {'form': form})

