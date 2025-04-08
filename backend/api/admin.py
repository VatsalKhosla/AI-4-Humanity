from django.contrib import admin
from .models import CropRecommendation,PredictionHistory,PlantDiseaseDetection

@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_crop', 'recommended_fertilizer', 'created_at')

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop', 'fertilizer', 'prediction_date')
    list_filter = ('crop', 'fertilizer', 'prediction_date')
    search_fields = ('user__username', 'crop', 'fertilizer')
    date_hierarchy = 'prediction_date'
    readonly_fields = ('prediction_date',)
    
    def get_soil_params(self, obj):
        return obj.soil_params
    get_soil_params.short_description = 'Soil Parameters'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'crop', 'fertilizer', 'prediction_date')
        }),
        ('Soil Parameters', {
            'fields': ('soil_params_json',),
            'classes': ('collapse',)
        }),
    )

@admin.register(PlantDiseaseDetection)
class PlantDiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = ('detected_disease', 'confidence_formatted', 'user', 'created_at')
    list_filter = ('detected_disease', 'created_at')
    search_fields = ('detected_disease', 'user__username', 'user__email')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def confidence_formatted(self, obj):
        """Format confidence as percentage"""
        return f"{obj.confidence:.2%}"
    confidence_formatted.short_description = 'Confidence'
    
    fieldsets = (
        ('Detection Information', {
            'fields': ('user', 'detected_disease', 'confidence', 'created_at')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Treatment', {
            'fields': ('treatment',)
        }),
    )
