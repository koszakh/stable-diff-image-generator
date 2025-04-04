from celery import shared_task
from .models import ImageGeneration
import torch
from diffusers import StableDiffusionPipeline

@shared_task
def generate_image_task(task_id):
    try:
        image_gen = ImageGeneration.objects.get(id=task_id)
        image_gen.status = 'processing'
        image_gen.save()

        model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        model.to("cuda" if torch.cuda.is_available() else "cpu")

        image = model(image_gen.prompt).images[0]
        image_path = f"generated/{task_id}.png"
        image.save(f"media/{image_path}")

        image_gen.result_image = image_path
        image_gen.status = 'completed'
        image_gen.save()
    except Exception as e:
        image_gen.status = 'failed'
        image_gen.save()
        print(f"Error {e}")

@shared_task
def test_task():
    print("Celery is working!")
    return "Success"