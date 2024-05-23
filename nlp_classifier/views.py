import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from transformers import RobertaForTokenClassification, AutoTokenizer, pipeline
from .models import Prediction
from django.utils import timezone
import time

# Load the tokenizer and model
original_model_name = "FacebookAI/roberta-base"
tokenizer = AutoTokenizer.from_pretrained(original_model_name, add_prefix_space=True)
model_name = "theglassofwater/NLP_GROUP13_ROBERTA_BASE"
model = RobertaForTokenClassification.from_pretrained(model_name)
token_classifier = pipeline("token-classification", model=model, tokenizer=tokenizer)

# logging configuration 
logging.basicConfig(filename='predictions.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def predict_(text):
    start_time = time.time()
    output = token_classifier(text)
    end_time = time.time()
    indexes = [[i["start"], i["end"]] for i in output]
    ner_tags = [i["entity"] for i in output]
    highlighting = [""] * len(text)
    for tag, range_ in zip(ner_tags, indexes):
        start, end = range_
        length = end - start
        new_tags = [tag] * length
        highlighting[start:end] = new_tags
    generate_time = end_time - start_time
    return ner_tags, indexes, highlighting, generate_time

@csrf_exempt
def predict(request):
    total_start_time = time.time()

    sentence = ""
    highlighted_sentence = ""
    tag_colors = {
        "B-O": "gray",
        "B-AC": "red",
        "B-LF": "green",
        "I-LF": "darkgreen",
        
    }

    if request.method == 'POST':
        data = request.POST.get('sentence')
        if data:
            sentence = data

            ner_tags, indexes, highlight, generate_time = predict_(data)  
            
            
            for char, tag in zip(sentence, highlight):
                color_class = tag_colors.get(tag, "black")
                highlighted_sentence += f'<span style="color: {color_class}">{char}</span>'
            
            # total time taken
            total_time = time.time() - total_start_time
            
            # Save prediction to database with ner_tags
            output_tags = " ".join(ner_tags)
            Prediction.objects.create(
                input_text=sentence,
                output_text=output_tags,
                total_time=total_time 
            )
            
        
            logging.info(f"Input: {sentence}, Output: {output_tags}, Created At: {timezone.now()}, Total Time: {total_time}")

    return render(request, 'index.html', {'sentence': sentence, 'prediction': highlighted_sentence, 'tag_colors': tag_colors})
