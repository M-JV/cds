from django.db import models

class TrainingData(models.Model):
    image = models.ImageField(upload_to='training_images/')
    label = models.CharField(max_length=3, default='no')  # "yes" or "no"
