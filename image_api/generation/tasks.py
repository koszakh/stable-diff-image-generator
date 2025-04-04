from celery import shared_task
from diffusers import StableDiffusionPipeline
from django.conf import settings
from .models import ImageGeneration
import os
import torch

@shared_task
def generate_image_task(task_id):
    try:
        image_gen = ImageGeneration.objects.get(id=task_id)
        image_gen.status = 'processing'
        image_gen.save()

        model_id = "CompVis/stable-diffusion-v1-4"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        model = StableDiffusionPipeline.from_pretrained(model_id)
        model.to(device)

        print(f"Generating image for prompt: {image_gen.prompt}")
        image = model(image_gen.prompt).images[0]

        relative_image_path = os.path.join('generated', f"{task_id}.png")
        full_image_path = os.path.join(settings.MEDIA_ROOT, relative_image_path)

        os.makedirs(os.path.dirname(full_image_path), exist_ok=True)

        print(f"Saving image to: {full_image_path}")
        image.save(full_image_path)

        image_gen.result_image.name = relative_image_path
        image_gen.status = 'completed'
        image_gen.save()
        print(f"Task {task_id} completed successfully.")

    except ImageGeneration.DoesNotExist:
        print(f"Task {task_id} failed: ImageGeneration object not found.")

    except Exception as e:
        print(f"Task {task_id} failed with error: {e}")
        try:
            image_gen = ImageGeneration.objects.get(id=task_id)
            image_gen.status = 'failed'
            image_gen.save()
        except ImageGeneration.DoesNotExist:
            pass
        except Exception as final_e:
            print(f"Could not update status to 'failed' for task {task_id}: {final_e}")

@shared_task
def test_task():
    print("Celery is working!")
    return "Success"