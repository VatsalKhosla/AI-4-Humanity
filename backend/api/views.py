from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import CropRecommendation
from crop_prediction.prediction import predict_crop, recommend_fertilizer
from .serializers import CropRecommendationSerializer
from .models import PlantDiseaseDetection
from users.models import User
from pest_recognition.recognition import recognizer, get_treatment_recommendation, PlantDiseaseRecognizer
from .serializers import PlantDiseaseDetectionSerializer
from api.models import PredictionHistory
from api.serializers import PredictionHistorySerializer
from django.conf import settings
import os
import json

# API endpoints for crop prediction
class CropPredictionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CropRecommendationSerializer
    
    def create(self, request, *args, **kwargs):
        # Get input parameters from request
        n = float(request.data.get('nitrogen', 0))
        p = float(request.data.get('phosphorus', 0))
        k = float(request.data.get('potassium', 0))
        ph = float(request.data.get('ph', 0))
        rainfall = float(request.data.get('rainfall', 0))
        humidity = float(request.data.get('humidity', 0))
        temperature = float(request.data.get('temperature', 0))
        
        # Make prediction
        crop = predict_crop(n, p, k, ph, rainfall, humidity, temperature)
        
        # Get fertilizer recommendation
        fertilizer = recommend_fertilizer(n, p, k, crop)

        soil_params = {
            'n': n,
            'p': p,
            'k': k,
            'ph': ph,
            'rainfall': rainfall,
            'humidity': humidity,
            'temperature': temperature
        }
        
        # Save to prediction history
        PredictionHistory.objects.create(
            user=request.user,
            crop=crop,
            fertilizer=fertilizer,
            soil_params_json=json.dumps(soil_params)
        )
        
        # Render result page
      
        # Create recommendation record
        user = User.objects.get(id=request.user.id)
        recommendation = CropRecommendation.objects.create(
            user=user,
            nitrogen=n,
            phosphorus=p,
            potassium=k,
            ph=ph,
            rainfall=rainfall,
            humidity=humidity,
            temperature=temperature,
            predicted_crop=crop,
            recommended_fertilizer=fertilizer
        )
        
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    





# API endpoints for disease detection
class PestRecognitionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlantDiseaseDetectionSerializer
    def create(self, request, *args, **kwargs):
        # Get image from request
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Save temporary image
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp', image.name)
        os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)
            
        with open(temp_image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Predict disease and confidence
        disease_name, confidence = recognizer.predict(temp_image_path)
        
        # Handle None response
        if disease_name is None:
            disease_name = "Unknown disease"
            confidence = 0.0
        
        # Get treatment recommendation
        treatment = get_treatment_recommendation(disease_name)
            
        try:
            # Create detection record
            detection = PlantDiseaseDetection.objects.create(
                user=request.user,
                image=image,
                detected_disease=disease_name,
                confidence=confidence,
                treatment=treatment
            )
            
            # Clean up temp file
            os.remove(temp_image_path)
                
            serializer = self.get_serializer(detection)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            # Clean up temp file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
            return Response({'error': f'Failed to save detection: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class PredictionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PredictionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user).order_by('-prediction_date')
    
'''

class PlantDiseaseRecognitionView(generics.CreateAPIView):
    """API view for plant disease recognition, following the same pattern as PestRecognitionView"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlantDiseaseDetectionSerializer
    
    def create(self, request, *args, **kwargs):
        # Get image from request
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save temporary image
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp', image.name)
        os.makedirs(os.path.dirname(temp_image_path), exist_ok=True)
        
        with open(temp_image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Predict disease and confidence using our recognizer
        disease_name, confidence = recognizer.predict(temp_image_path)
        
        if not disease_name or not confidence:
            # Clean up temp file
            os.remove(temp_image_path)
            return Response(
                {'error': 'Failed to process image or detect disease'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get treatment recommendation
        treatment = get_treatment_recommendation(disease_name)
        
        # Create detection record
        detection = PlantDiseaseDetection.objects.create(
            user=request.user,
            image=image,
            detected_disease=disease_name,
            confidence=confidence,
            treatment=treatment
        )
        
        # Clean up temp file
        os.remove(temp_image_path)
        
        serializer = self.get_serializer(detection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  '''