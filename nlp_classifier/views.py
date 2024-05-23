from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def classify_sentence(sentence):
    tokens = sentence.split()
    tags = ['B-O'] * len(tokens)  # Dummy tags for demonstration
    return list(zip(tokens, tags))

@csrf_exempt
def predict(request):
    prediction = None
    if request.method == 'POST':
        data = request.POST.get('sentence')
        if data:
            prediction = classify_sentence(data)
    return render(request, 'index.html', {'prediction': prediction})
