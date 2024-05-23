from django.db import models
from django.utils import timezone

class Prediction(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    total_time = models.FloatField(default=0.0)  

    def __str__(self):
        return f"Prediction {self.id} at {self.created_at}"
