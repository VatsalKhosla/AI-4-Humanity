import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from skimage import io
from skimage.transform import resize
from skimage import img_as_ubyte
from django.conf import settings

class PlantDiseaseRecognizer:
    """Helper class for loading the model and making predictions"""
    def __init__(self):
        self.model = None
        self.categories = [
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
            'Corn_(maize)___Common_rust_',
            'Corn_(maize)___healthy',
            'Peach___Bacterial_spot',
            'Peach___healthy'
        ]
        self.img_size = 28
        self.load_model()
    
    def load_model(self):
        """Load the trained model from .h5 file"""
        model_path = os.path.join(settings.BASE_DIR, 'plant_disease_model.h5')
        try:
            self.model = load_model(model_path)
            print("Model loaded successfully from:", model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def preprocess_image(self, image_path):
    
        try:
        # Read image using skimage with error handling
            try:
                img_array = io.imread(image_path)
                print(f"Image successfully read, shape: {img_array.shape}")
            except Exception as e:
                print(f"Error reading image with skimage: {e}")
                # Fallback to PIL
                from PIL import Image
                import numpy as np
                img = Image.open(image_path)
                img_array = np.array(img)
                print(f"Image read with PIL, shape: {img_array.shape}")
            
            # Handle different image formats
                if len(img_array.shape) == 2:
                    # Convert grayscale to RGB
                    print("Converting grayscale to RGB")
                    img_array = np.stack((img_array,)*3, axis=-1)
                elif img_array.shape[2] == 4:
                    # Handle RGBA images
                    print("Removing alpha channel from RGBA image")
                    img_array = img_array[:,:,:3]
                
                # Convert color channels to match training preprocessing
                img_array = img_array[:, :, ::-1]
                print(f"After color channel conversion, shape: {img_array.shape}")
                
                # Resize to 28x28 as in the training code
                new_array = resize(img_array, (self.img_size, self.img_size))
                new_array = img_as_ubyte(new_array)
                print(f"After resize, shape: {new_array.shape}")
                
                # Normalize to match training preprocessing
                new_array = new_array.astype('float32')
                new_array = new_array / 255.0
                
                # Reshape for the model (batch, width, height, channels)
                processed_img = new_array.reshape(-1, self.img_size, self.img_size, 3)
                print(f"Final processed shape: {processed_img.shape}")
                
                return processed_img
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def predict(self, image_path):
        """Make prediction on the given image"""
        if self.model is None:
            return None, None
        
        processed_img = self.preprocess_image(image_path)
        if processed_img is None:
            return None, None
        
        try:
            # Make prediction
            predictions = self.model.predict(processed_img)[0]
            
            # Get predicted class and confidence
            predicted_class_index = np.argmax(predictions)
            confidence = float(predictions[predicted_class_index])
            predicted_class = self.categories[predicted_class_index]
            
            return predicted_class, confidence
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None, None


# Create a singleton instance
recognizer = PlantDiseaseRecognizer()


def get_treatment_recommendation(disease_name):
    """Return treatment recommendation based on detected disease"""
    treatments = {
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 
            "Apply fungicides containing pyraclostrobin, azoxystrobin, trifloxystrobin, or picoxystrobin. Rotate crops and remove crop debris.",
        
        'Corn_(maize)___Common_rust_': 
            "Apply fungicides with active ingredients like azoxystrobin, pyraclostrobin, or trifloxystrobin. Plant resistant corn varieties.",
        
        'Corn_(maize)___healthy': 
            "No treatment needed. Continue regular maintenance and monitoring.",
        
        'Peach___Bacterial_spot': 
            "Apply copper-based bactericides in early spring. Prune infected branches and ensure good air circulation.",
        
        'Peach___healthy': 
            "No treatment needed. Continue regular maintenance and monitoring."
    }
    
    return treatments.get(disease_name, "Consult with a plant pathologist for specific recommendations.")
