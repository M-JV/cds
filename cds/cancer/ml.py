import os
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf

def predict_tumor(image_path):
    encoder = OneHotEncoder()
    encoder.fit([[0], [1]])

    dataset_dir = '/home/mejova/cds/dataset'  # Update the dataset directory path

    data = []
    result = []

    try:
        tumor_dir = os.path.join(dataset_dir, 'yes')
        for file in os.listdir(tumor_dir):
            if file.endswith('.jpg'):
                path = os.path.join(tumor_dir, file)
                img = Image.open(path)
                img = img.resize((128, 128))
                img = np.array(img)
                if img.shape == (128, 128, 3):
                    data.append(img)
                    result.append(encoder.transform([[0]]).toarray())

        no_tumor_dir = os.path.join(dataset_dir, 'no')
        for file in os.listdir(no_tumor_dir):
            if file.endswith('.jpg'):
                path = os.path.join(no_tumor_dir, file)
                img = Image.open(path)
                img = img.resize((128, 128))
                img = np.array(img)
                if img.shape == (128, 128, 3):
                    data.append(img)
                    result.append(encoder.transform([[1]]).toarray())

        data = np.array(data)
        result = np.array(result)

        x_train, x_test, y_train, y_test = train_test_split(data, result, test_size=0.2, shuffle=True, random_state=0)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, kernel_size=(2, 2), input_shape=(128, 128, 3), padding='same'),
            tf.keras.layers.Conv2D(32, kernel_size=(2, 2), activation='relu', padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Conv2D(64, kernel_size=(2, 2), activation='relu', padding='same'),
            tf.keras.layers.Conv2D(64, kernel_size=(2, 2), activation='relu', padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(2, activation='softmax')
        ])

        model.compile(loss="categorical_crossentropy", optimizer='adamax')

        print(model.summary())

        y_train = np.squeeze(y_train)
        y_test = np.squeeze(y_test)

        history = model.fit(x_train, y_train, epochs=30, batch_size=40, verbose=1, validation_data=(x_test, y_test))

        def names(number):
            if number == 0:
                return 'Tumor'
            else:
                return 'No Tumor'

        img = Image.open(image_path)
        x = np.array(img.resize((128, 128)))
        x = x.reshape(1, 128, 128, 3)
        res = model.predict_on_batch(x)
        classification = np.argmax(res, axis=1)[0]
        confidence = str(res[0][classification] * 100)
        result = names(classification)
        return f"{result} with {confidence}% confidence"
    except FileNotFoundError:
        return "Dataset directory not found or does not exist"

# Example usage
image_path = input("Enter the path to the image: ")
prediction = predict_tumor(image_path)
print(prediction)
