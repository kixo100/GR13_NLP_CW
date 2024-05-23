from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from transformers import RobertaForTokenClassification, AutoTokenizer, pipeline
from torch import load, device

original_model_name = "FacebookAI/roberta-base"
tokenizer = AutoTokenizer.from_pretrained(original_model_name, add_prefix_space=True,)

model_name = "theglassofwater/NLP_GROUP13_ROBERTA_BASE"
model = RobertaForTokenClassification.from_pretrained(model_name)
print(model)
token_classifier = pipeline(
"token-classification", model=model, tokenizer=tokenizer
)

def predict_(text):
    output = token_classifier(text)
    indexes = [[i["start"], i["end"]] for i in output]
    ner_tags = [i["entity"] for i in output]
    highlighting = [""]*len(text)
    for tag, range in zip(ner_tags, indexes):
        start, end = range
        length = end-start
        new_tags = [tag]*length
        highlighting[start:end] = new_tags
    return ner_tags #, indexes, highlighting

# def classify_sentence(sentence):
#     tokens = sentence.split()
#     tags = ['B-O'] * len(tokens)  # Dummy tags for demonstration
#     return list(zip(tokens, tags))

@csrf_exempt
def predict(request):
    prediction = None
    if request.method == 'POST':
        data = request.POST.get('sentence')
        if data:
            prediction = predict_(data)
        
    return render(request, 'index.html', {'prediction': prediction})
