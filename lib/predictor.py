import os

def predict_fire(model, test_images, test_folder, preprocess_image):
    """
    Predicts fire presence in a list of test images using a trained model.

    Args:
    - model: Trained machine learning model.
    - test_images: List of image filenames.
    - test_folder: Path to the folder containing test images.
    - preprocess_image: Function to preprocess an image before prediction.
    """
    for img_name in test_images:
        img_path = os.path.join(test_folder, img_name)
        img_array = preprocess_image(img_path)
        prediction = model.predict(img_array)[0][0]
        predicted_class = 'Fire' if prediction > 0.5 else 'No Fire'
        confidence = prediction if prediction > 0.5 else 1 - prediction

        print(f"Image: {img_name}, Predicted: {predicted_class}, Confidence: {confidence:.2f}")

