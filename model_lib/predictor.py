import numpy as np

def predict_image(model, image_path, target_size=(350, 350)):
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)[0][0]
    predicted_class = 'Fire' if prediction > 0.5 else 'No Fire'
    confidence = prediction if prediction > 0.5 else 1 - prediction
    
    return predicted_class, confidence
