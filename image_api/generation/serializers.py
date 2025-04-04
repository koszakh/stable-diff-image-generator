from rest_framework import serializers
from .models import ImageGeneration

class ImageGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGeneration
        fields = '__all__'