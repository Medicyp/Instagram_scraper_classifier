import cv2
import requests
from PIL import Image
from io import BytesIO

import numpy as np

age_list = ['0-2', '4-6', '8-12', '15-20', '25-32', '38-43', '48-53', '60-100']
gender_list = ['male', 'female']


# Replace the URL with the URL of the image you want to use
woman_waterfall_url = 'https://scontent-lhr8-2.cdninstagram.com/v/t51.2885-19/280599842_123615616995577_1519849987580569477_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-lhr8-2.cdninstagram.com&_nc_cat=101&_nc_ohc=EeCf9Gt1q0QAX-3Jdd9&edm=APQMUHMBAAAA&ccb=7-5&oh=00_AfDVXgvIZdldhaICBFpuW6XKDiUOGcXoOBW6HkqRp_w0rg&oe=63A66B94&_nc_sid=e5d0a6'
man_with_glasses_url = 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50'
woman_staring_url = 'https://images.unsplash.com/photo-1597223557154-721c1cecc4b0?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80'
old_woman_url = 'https://media.sciencephoto.com/image/f0051122/800wm/F0051122-Close_up_of_older_woman_s_face.jpg'
old_man_smiling_url = 'https://images.unsplash.com/photo-1601600415813-e6063ad12335?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80'
man_url = 'https://i.pinimg.com/736x/25/1b/c1/251bc1f03f23cc865d6a21e83efc02f8.jpg'
teenager_man_url = 'https://images.medicinenet.com/images/article/main_image/how-do-i-deal-with-my-14-year-old-son.jpg'

# Choose your url:
image_url = teenager_man_url

# Download the image and convert it to a format that can be processed by OpenCV
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
image = image.convert('RGB')
image_np = np.array(image)

# Load the models for estimating age and gender
age_model_path = 'models/super_age_model.caffemodel'
age_weights_path = 'models/super_age_model.prototxt'
age_model = cv2.dnn.readNetFromCaffe(age_weights_path, age_model_path)

gender_model_path = 'models/super_gender_model.caffemodel'
gender_weights_path = 'models/super_gender_model.prototxt'
gender_model = cv2.dnn.readNetFromCaffe(gender_weights_path, gender_model_path)

# Use the models to estimate the age and gender of the person in the image
age_blob = cv2.dnn.blobFromImage(image_np, size=(227, 227), ddepth=cv2.CV_8U)
age_model.setInput(age_blob)
age_predictions = age_model.forward()
age = age_list[age_predictions[0].argmax()]

gender_blob = cv2.dnn.blobFromImage(image_np, size=(227, 227), ddepth=cv2.CV_8U)
gender_model.setInput(gender_blob)
gender_predictions = gender_model.forward()
gender = gender_list[gender_predictions[0].argmax()]

# Print the results
print(f'Age: {age}')
print(f'Gender: {gender}')
