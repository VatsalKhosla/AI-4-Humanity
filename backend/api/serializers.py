from rest_framework import serializers
from api.models import CropRecommendation
from .models import PlantDiseaseDetection
from .models import PredictionHistory

class CropRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropRecommendation
        fields = '__all__'
        read_only_fields = ['predicted_crop', 'recommended_fertilizer', 'user']



class PlantDiseaseDetectionSerializer(serializers.ModelSerializer):
    """Serializer for plant disease detection results"""
    image_url = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = PlantDiseaseDetection
        fields = [
            'id', 'image_url', 'detected_disease', 'confidence', 
            'treatment', 'created_at', 'username'
        ]
        read_only_fields = ['detected_disease', 'confidence', 'treatment']
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_username(self, obj):
        return obj.user.username


class PredictionHistorySerializer(serializers.ModelSerializer):
    soil_params = serializers.SerializerMethodField()
    
    class Meta:
        model = PredictionHistory
        fields = ['id', 'prediction_date', 'crop', 'fertilizer', 'soil_params']
    
    def get_soil_params(self, obj):
        return obj.soil_params