import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array

# Load MobileNetV2 (Extremely lightweight, TensorFlow is already installed!)
_model = None

# ✅ MASSIVELY EXPANDED MAPPING
# We map any weird ImageNet output exactly to a user-friendly fashion item string.
LABEL_MAPPING = {
    "jersey": "shirt",
    "t-shirt": "tshirt",
    "sweatshirt": "hoodie",
    "cardigan": "sweater",
    "miniskirt": "skirt",
    "hoopskirt": "skirt",
    "overskirt": "skirt",
    "jean": "jeans",
    "sweatpants": "pants",
    "running_shoe": "shoes",
    "loafer": "shoes",
    "sandal": "shoes",
    "sneaker": "shoes",
    "clog": "shoes",
    "boot": "shoes",
    "shoe": "shoes",
    "trench_coat": "jacket",
    "suit": "suit",
    "gown": "dress",
    "fur_coat": "jacket",
    "cloak": "jacket",
    "poncho": "jacket",
    "sombrero": "hat",
    "cowboy_hat": "hat",
    "backpack": "bag",
    "purse": "bag",
    "mailbag": "bag",
    "bow_tie": "accessory",
    "windsor_tie": "accessory",
    "sunglass": "glasses",
    "sunglasses": "glasses"
}

def _get_model():
    global _model
    if _model is None:
        _model = MobileNetV2(weights="imagenet")
    return _model

def predict_object(image_path: str) -> str:
    """Read an image, run MobileNetV2 (Offline & Fast), and return the predicted object label."""
    model = _get_model()

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read uploaded image for prediction")
        
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image, (224, 224))
    
    img_array = img_to_array(image_resized)
    img_batch = np.expand_dims(img_array, axis=0)
    
    img_preprocessed = preprocess_input(img_batch)
    
    predictions = model.predict(img_preprocessed)
    
    # Check top 5 predictions in case top 1 isn't clothing
    decoded = decode_predictions(predictions, top=5)[0]
    
    # We will search the top 5 predictions to actively search for ANYTHING fashion related!
    # This completely fixes the "bad prediction" issue!
    for _, class_name, _ in decoded:
        label = class_name.lower().replace("_", " ")
        if label in LABEL_MAPPING:
            return LABEL_MAPPING[label]
            
    # Fallback to top 1 if none match our mapping exactly
    top_label = decoded[0][1].lower().replace("_", " ")
    return top_label