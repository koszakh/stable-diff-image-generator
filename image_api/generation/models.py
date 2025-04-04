from django.db import models

class ImageGeneration(models.Model):
    prompt = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    result_image = models.ImageField(upload_to='generated/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)