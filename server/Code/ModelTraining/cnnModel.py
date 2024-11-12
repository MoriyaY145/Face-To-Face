import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras import layers, models


# Load data from CSV file # y
data = pd.read_csv('../../data/ExcelKeyPoints/all_data.csv')
image_height, image_width = 64, 64
num_channels = 3
image_paths = data.iloc[:, 0]
# Load images and preprocess
images = [img_to_array(load_img(f'../../data/ImagesDataCnn/{path}', target_size=(image_height, image_width))) for path in image_paths]
x = np.array(images) / 255.0  # Normalize pixel values to [0, 1]
y = data.iloc[:, 1:]

X_train, X_val, y_train, y_val = train_test_split(x, y, test_size=0.1, random_state=42)
X_test, X_val, y_test, y_val = train_test_split(X_val, y_val, test_size=0.1, random_state=42)


# Define the CNN model
model = models.Sequential()
# Add convolutional layers
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_height, image_width, num_channels)))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))

# Flatten the output and add dense layers
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(136, activation='linear'))  # Output layer with 136 neurons

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')  # Use appropriate loss function based on your task

# Print the model summary
model.summary()

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=500, batch_size=64)
model.save('..\..\models\cnnKeyPoints.h5')