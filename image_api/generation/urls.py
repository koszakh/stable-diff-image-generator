from django.urls import path
from .views import GenerateImageView, GetImageStatusView

urlpatterns = [
    path('generate/', GenerateImageView.as_view(), name='generate'),
    path('status/<int:task_id>/', GetImageStatusView.as_view(), name='status'),
]