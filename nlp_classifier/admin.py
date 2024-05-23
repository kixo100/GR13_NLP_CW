from django.contrib import admin
from .models import Prediction
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nlp_classifier.urls')),
]

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('input_text', 'created_at')
    search_fields = ('input_text', 'output_text')
