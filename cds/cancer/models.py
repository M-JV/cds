from django.db import models

class TrainingData(models.Model):
    image = models.ImageField(upload_to='training_images')
    prediction_result = models.CharField(max_length=100)  # Adjust the field type as per your requirement

    def __str__(self):
        return f"TrainingData: {self.image}"
