from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def load_model():
    # Load your model here (e.g., using joblib or pickle)
    import joblib
    model = joblib.load('classifier/model.pkl')
    return model

model = load_model()

@csrf_exempt
def predict(request):
    prediction = None
    if request.method == 'POST':
        data = json.loads(request.body)
        sentence = data['sentence']
        # Your model's prediction logic here
        prediction = model.predict([sentence])[0]  # Modify according to your model
    return JsonResponse({'prediction': prediction})


    from django.shortcuts import render
from .utils import load_model

model = load_model()

def classify_sentence(sentence):
    # Your model's prediction logic here
    tokens = sentence.split()
    tags = ['B-O'] * len(tokens)  # Dummy tags for demonstration
    return list(zip(tokens, tags))

def predict(request):
    prediction = None
    if request.method == 'POST':
        sentence = request.POST.get('sentence')
        prediction = classify_sentence(sentence)
    return render(request, 'index.html', {'prediction': prediction})

