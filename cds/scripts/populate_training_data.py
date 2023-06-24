import os
from django.core.files import File
from cancer.models import TrainingData

def populate_training_data():
    dataset_path = '/home/mejova/cds//dataset'

    yes_dir = os.path.join(dataset_path, 'yes')
    no_dir = os.path.join(dataset_path, 'no')

    for filename in os.listdir(yes_dir):
        image_path = os.path.join(yes_dir, filename)
        with open(image_path, 'rb') as f:
            image_file = File(f)
            TrainingData.objects.create(image=image_file, label='Y')

    for filename in os.listdir(no_dir):
        image_path = os.path.join(no_dir, filename)
        with open(image_path, 'rb') as f:
            image_file = File(f)
            TrainingData.objects.create(image=image_file, label='no')
