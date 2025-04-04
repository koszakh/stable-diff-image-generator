from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImageGeneration
from .serializers import ImageGenerationSerializer
from .tasks import generate_image_task

class GenerateImageView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        image_gen = ImageGeneration.objects.create(prompt=prompt)
        generate_image_task.delay(image_gen.id)

        return Response({"task_id": image_gen.id, "status": "pending"}, status=status.HTTP_202_ACCEPTED)

class GetImageStatusView(APIView):
    def get(self, request, task_id):
        try:
            image_gen = ImageGeneration.objects.get(id=task_id)
            return Response(ImageGenerationSerializer(image_gen).data)
        except ImageGeneration.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)