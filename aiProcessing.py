import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image


# Load the trained model
def modelLoad():
    model = load_model('models/trashnet_model.h5')
    return model

model = modelLoad()

#Determine which class is which object
class_labels = ['Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic', 'Trash']

def analyseImage(image_url):
    # Load and preprocess the image
    image = Image.open(image_url)
    image = image.resize((224, 224))  # Resize the image to match the input size of the model
    image_array = np.array(image) / 255.0  # Normalize the pixel values

    # Expand dimensions to match the input shape of the model
    input_image = np.expand_dims(image_array, axis=0)

    # Make predictions
    predictions = model.predict(input_image)

    # Get the predicted class index
    predicted_class_index = np.argmax(predictions[0])

    # Map the predicted class index to the corresponding label
    predicted_class = class_labels[predicted_class_index]

    return ("Predicted class:", predicted_class)